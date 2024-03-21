package me.kunalbhagawati

import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.core.FuelError
import com.github.kittinunf.fuel.core.extensions.jsonBody
import com.github.kittinunf.fuel.serialization.responseObject
import com.github.kittinunf.result.Result
import com.github.kittinunf.result.flatMap
import io.github.cdimascio.dotenv.dotenv
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import net.lingala.zip4j.ZipFile
import java.io.File

val dotenv = dotenv()


@Serializable
data class HackatticData(
  @SerialName("zip_url") val zipUrl: String,
)

@Serializable
data class HackatticSolution(
  val secret: String
)

fun getData(): Result<HackatticData, FuelError> =
  Fuel
    .get(Constants.FETCH_PROBLEM_INPUTS_URL.replace(mapOf("ACCESS_TOKEN" to dotenv["ACCESS_TOKEN"])))
    .responseObject<HackatticData>()
    .let { (_, _, result) -> result }

fun fetchZip(data: HackatticData): Result<ZipFile, Exception> =
  Fuel
    .get(data.zipUrl)
    .response()
    .let { (_, _, result: Result<ByteArray, FuelError>) ->
      fun toZipFile(arr: ByteArray): ZipFile =
        File("")
          .apply { appendBytes(arr) }
          .let { ZipFile(it) }

      return result.flatMap { Result.of(toZipFile(it)) }
    }

fun getSecret(file: ZipFile): Result<String, Exception> {
  runBlocking {
    launch {}
  }
}

fun postSolution(secret: String) =
  Fuel
    .post(Constants.SUBMIT_SOLUTION_URL.replace(mapOf("ACCESS_TOKEN" to dotenv["ACCESS_TOKEN"])))
    .jsonBody(Json.encodeToString(HackatticSolution))
    .response()
    .let { (_, _, result) -> result }

fun main() {
  getData()
    .flatMap { fetchZip(it) }
    .flatMap { getSecret(it) }
    .flatMap { postSolution(it) }
    .fold(::println, ::println)
}
