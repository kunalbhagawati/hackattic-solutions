import http, { IncomingMessage, RequestListener } from 'http'
import jwt from 'jwt-simple'
import axios from 'axios'
import { isEmpty } from 'ramda'

const PROBLEM_NAME = 'jotting_jwts'
const HOST = 'https://hackattic.com'
const CHALLENGE_PATH = `challenges/${PROBLEM_NAME}` // This is a pure string.
const FETCH_PROBLEM_INPUTS_URL = `${HOST}/${CHALLENGE_PATH}/problem?access_token=${process.env.ACCESS_TOKEN}`
const SUBMIT_SOLUTION_URL = `${HOST}/${CHALLENGE_PATH}/solve?access_token=${process.env.ACCESS_TOKEN}`

// Usually globals are a very bad idea, but we'll manage for now.
let SOLUTION_STRING = ''
let JWT_SECRET: string

type JwtPayload = {
  append: string
}

/**
 * Get the payload as a string from the request body.
 *
 * The trick here is that the request headers don't have `Content-Type`.
 * Since `http` doesn't do body parsing by default, and all content negotiation libraries explicitly require
 * the `Content-Type` header to work properly, we need to parse the body ourselves explicitly.
 */
const getJwtPayload = async (req: IncomingMessage): Promise<string> => {
  const buffers = []

  for await (const chunk of req) {
    buffers.push(chunk)
  }

  const jwt_payload = Buffer.concat(buffers).toString()
  console.log(`RECEIVED JWT: ${jwt_payload}`)
  return jwt_payload
}

/**
 * Receive the requests from hackattic and reply appropriately _while_ adding to the solution string if applicable.
 */
const requestListener: RequestListener = async (req, res) => {
  const jwtPayload = await getJwtPayload(req)

  const replyWithSolution = () =>
    res.writeHead(200, { 'Content-Type': 'application/json' }).end(JSON.stringify({ solution: SOLUTION_STRING }))

  const appendToSolutionAndReply = (decoded: JwtPayload) => {
    SOLUTION_STRING += decoded['append']
    res.writeHead(200).end()
  }

  let decoded

  try {
    decoded = jwt.decode(jwtPayload, JWT_SECRET) as JwtPayload
    console.log(decoded)
  } catch (e) {
    console.log(`ERROR: ${e}`)
    res.writeHead(200).end()
    return
  }

  if (isEmpty(decoded)) {
    console.log('FOUND EMPTY PAYLOAD. REPLYING WITH SOLUTION')
    replyWithSolution()
  } else {
    appendToSolutionAndReply(decoded)
  }
}

/**
 * Creates a listening web server to handle hackattic requests.
 */
const createServer = (port: number, host: string) => {
  const server = http.createServer(requestListener)
  server.listen(port, host, () => console.log(`Server running on ${host}@${port}`))
  return server
}

const main = async () => {
  const res = await axios.get(FETCH_PROBLEM_INPUTS_URL)
  JWT_SECRET = res.data.jwt_secret
  console.log(`JWT SECRET: ${JWT_SECRET}`)

  createServer(
    parseInt(process.env.JOTTING_JWTS__SERVER_PORT as string),
    process.env.JOTTING_JWTS__SERVER_HOST as string,
  )

  await axios.post(SUBMIT_SOLUTION_URL, { app_url: process.env.PUBLIC_ADDRESS, solution: SUBMIT_SOLUTION_URL })
}

main()
