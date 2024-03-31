/**
 * This does not work.
 * `scrypt` fails on a very large `N` number.
 */
import axios from "axios";
import crypto, {Hash, Hmac, ScryptOptions} from "crypto";

const PROBLEM_NAME = 'password_hashing'
const HOST = 'https://hackattic.com'
const CHALLENGE_PATH = `challenges/${PROBLEM_NAME}` // This is a pure string.
const FETCH_PROBLEM_INPUTS_URL = `${HOST}/${CHALLENGE_PATH}/problem?access_token=${process.env.ACCESS_TOKEN}`
const SUBMIT_SOLUTION_URL = `${HOST}/${CHALLENGE_PATH}/solve?access_token=${process.env.ACCESS_TOKEN}`


type HackatticOptions = {
  password: string,
  salt: string,
  pbkdf2: {
    hash: string,
    rounds: number,
  },
  scrypt: {
    N: number,
    p: number,
    r: number,
    buflen: number,
    _control: string,
  },
}

type Hashes = {
  sha256: Hash
  hmac: Hmac
  pbkdf2: Buffer
  scrypt: Buffer,
}

const generateHashes = (options: HackatticOptions): Hashes => {
  const salt_decoded = Buffer.from(options.salt, 'base64')

  const sha256 = crypto.createHash('sha256').update(options.password)
  const hmac = crypto.createHmac('sha256', salt_decoded).update(options.password);

  const {rounds, hash} = options.pbkdf2;
  const pbkdf2 = crypto.pbkdf2Sync(options.password, salt_decoded, rounds, 32, hash);

  const scrypt_control = crypto.scryptSync("rosebud", "pepper", 32, {N: 128, p: 8, r: 4})
  const scrypt_control_hex = 'b19a18ea8a50a861d08eb94be602f6cbfe67ab98d2021400a3b83fbe3b8ba698'
  if (scrypt_control_hex !== scrypt_control.toString('hex')) throw "Control fail"

  const {N, r, p, buflen} = options.scrypt;
  const scrypt_options: ScryptOptions = {N: N, p, r}

  const scrypt = crypto.scryptSync(options.password, salt_decoded, buflen, scrypt_options)

  return {sha256, hmac, pbkdf2, scrypt}
}

const main = async () => {
  const res = await axios.get<HackatticOptions>(FETCH_PROBLEM_INPUTS_URL)
  const hashes = generateHashes(res.data)
  await submit(hashes)
}

const submit = async ({hmac, pbkdf2, scrypt, sha256}: Hashes) => {
  const data = {
    sha256: sha256.digest('hex'),
    hmac: hmac.digest('hex'),
    pbkdf2: pbkdf2.toString('hex'),
    scrypt: scrypt.toString('hex'),
  }
  const res = await axios.post(SUBMIT_SOLUTION_URL, data)
  console.log(res.data)
}

main()
