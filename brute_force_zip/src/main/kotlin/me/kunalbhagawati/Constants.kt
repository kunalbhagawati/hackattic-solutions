package me.kunalbhagawati

object Constants {
  private const val PROBLEM_NAME = "brute_force_zip"

  private const val HOST = "https://hackattic.com"
  private const val CHALLENGE_PATH = "challenges/${PROBLEM_NAME}"  // This is a pure string.

  private const val HOST_CHALLENGE_PATH = "${HOST}/${CHALLENGE_PATH}"

  val FETCH_PROBLEM_INPUTS_URL = Template("${HOST_CHALLENGE_PATH}/problem?access_token={ACCESS_TOKEN}")
  val SUBMIT_SOLUTION_URL = Template("${HOST_CHALLENGE_PATH}/solve?access_token={ACCESS_TOKEN}")
}
