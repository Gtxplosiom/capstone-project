def execute(command):
    print(command)

def process_commands(string: str):
    keywords = ['Open', 'Close', 'Search']

    commands = []

    words = string.split()

    for word in words:
        if word in keywords:
            word_index = words.index(word)
            command_index = keywords.index(word)

            if word == 'Search':
                query = words[word_index + 1:]

                for x in query:     # check if there are keywords in the query
                    if x in keywords:
                        exclude_index = query.index(x)

                query = query[:exclude_index]      # omit the keyword found and the rest of the text that follows it

                query = ' '.join(query)

                command = f'{words[word_index]} {query}'
                words.remove(words[word_index])
            else:
                command = f'{words[word_index]} {words[word_index + 1]}'

                words.remove(words[word_index + 1])     # the following word which is 'browser' is removed first because if the reference word 'Open' is removed first it will cause problems and not remove the following word in result
                words.remove(words[word_index])

            commands.append(command)

    for command in commands:
        execute(command)

sample_string = 'I am Gtxplosion and I want to Open browser and Search one piece is the best of all time ever Open link'

process_commands(sample_string)