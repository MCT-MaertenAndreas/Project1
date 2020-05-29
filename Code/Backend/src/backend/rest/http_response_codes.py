success_code = {
    204: ('', 204)
}

error_code = {
    400: ('<pre>400 - Bad Request<br><br>The server could not understand the request due to invalid syntax of the URL or certain HEADERS were missing.</pre>', 400),
    401: ('<pre>401 - Unauthorized<br><br>The client failed to authenticate thus there was no response body.</pre>', 401),
    403: ('<pre>403 - Forbidden<br><br>The client does not have access rights to the content.</pre>', 403),
    404: ('<pre>404 - Not Found<br><br>The requested URL was not found on this server.</pre>', 404),
    405: ('<pre>405 - Method Not Allowed<br><br>The given URL exists but an invalid request method was used.</pre>', 405),

    500: ('<pre>500 - Unexpected Error<br><br>An unexpected error occured.</pre>', 500)
}
