package me.kunalbhagawati

/**
 * Acts like a string template in python or ruby, where we define placeholders and can substitute them later.
 *
 * TODO Replace this with something already existing inside the language.
 */
class Template(val string: String) {
    /** Returns the placeholders in order of their defined position in the [string] */
    val placeholders get(): List<String> = TODO()

    /** Replace the values in [string] with the [values] given, matching the key to the value in the map. */
    fun replace(values: Map<String, Any>): String =
        values
            .toList()
            .fold(string) { acc, (k, v) -> acc.replace("{$k}", v.toString()) }
}
