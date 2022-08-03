import axios, { AxiosResponse } from 'axios'
import { createHash } from 'crypto'
import { __, curry } from 'ramda'

const PROBLEM_NAME = 'mini_miner'
const HOST = 'https://hackattic.com'
const CHALLENGE_PATH = `challenges/${PROBLEM_NAME}` // This is a pure string.
const FETCH_PROBLEM_INPUTS_URL = `${HOST}/${CHALLENGE_PATH}/problem?access_token=${process.env.ACCESS_TOKEN}`
const SUBMIT_SOLUTION_URL = `${HOST}/${CHALLENGE_PATH}/solve?access_token=${process.env.ACCESS_TOKEN}`

type Block = {
  nonce: null
  data: Array<[string, number]>
}

type Response = {
  difficulty: number
  block: Block
}

const fetchProblemSet = async () => {
  try {
    const response: AxiosResponse<Response> = await axios.get(FETCH_PROBLEM_INPUTS_URL)
    return response.data
  } catch ({ data }) {
    throw new Error(`Failed to fetch data from h^.\n${data}`)
  }
}

const submitResponse = async (nonce: number) => await axios.post(SUBMIT_SOLUTION_URL, { nonce })

/** Create a SHA256 from the given string and check if it has difficulty number of bits in the beginning. */
const shaMatchesDifficulty = (s: string, difficulty: number) => {
  const hash = createHash('sha256').update(s, 'utf-8')
  const d = hash.digest('hex')
  const dInBinary = BigInt(`0x${d}`).toString(2)
  return 256 - dInBinary.length === difficulty
}

/** Check if the nonce value matches the hash. */
const tryWithNonce = async (block: Block, nonce: number, difficulty: number): Promise<boolean> => {
  const newBlock = { ...block, nonce: nonce }
  const jsonified = JSON.stringify(newBlock, Object.keys(newBlock).sort(), 0)
  return shaMatchesDifficulty(jsonified, difficulty)
}

const main = async () => {
  const data = await fetchProblemSet()

  const block = data.block

  const curried = curry(tryWithNonce)(block, __, data.difficulty)

  let nonce = 0

  while (nonce > -1) {
    if (await curried(nonce)) {
      const response = await submitResponse(nonce)
      console.log(response.data)
      break
    }

    nonce += 1
  }
}

main()
