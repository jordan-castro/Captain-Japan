using PyCall

"""
Return the chapter url of the current url.

Args:
    current_url (str): The current url.

Returns: str 
"""
function chapterurl(current_url, types, values)
    url = current_url
    # Check if the current url has arguments arleady.
    if occursin("?", url)
        # Strip em
        url = split(url, "?")[1]
    end
    args = ""
    # Create the url.
    for i in 1:length(types)
        ampersand = "&"
        # CHeck if ampersand is needed
        if i == 1 || i == length(types)
            ampersand = ""
        end
        # Are we at the end of values?
        if i > length(values)
            break
        end

        # println(types[i])
        # println(values[i])

        value = tryparse(Int, values[i])
        # Check if value is number
        if value !== nothing
            args = args * "$(ampersand)$(types[i])=$(value + 1)"
        else
            args = args * "$(ampersand)$(types[i])=$(values[i])"
        end
    end

    # Return the url.
    return "$url?$args"
end