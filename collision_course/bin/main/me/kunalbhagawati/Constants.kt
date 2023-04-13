package me.kunalbhagawati

object Constants {
    const val PROBLEM_NAME = "collision_course"

    const val HOST = "https://hackattic.com"
    val CHALLENGE_PATH = Template("challenges/${PROBLEM_NAME}")  // This is a pure string.
    val FETCH_PROBLEM_INPUTS_URL = Template("${HOST}/${CHALLENGE_PATH}/problem?access_token={ACCESS_TOKEN}")
    val SUBMIT_SOLUTION_URL = Template("${HOST}/${CHALLENGE_PATH}/solve?access_token={ACCESS_TOKEN}")
}
