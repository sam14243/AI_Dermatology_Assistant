def get_chat_history_buffer_memory(history):
    num = len(history)
    mes = []
    if num>1:
        i = num - 1
        max_num = 1
        l = ""

        while i > 0 and max_num < 10:
            j = i-1
            mes.append({'role': "user", "content" : history[i]['content']}, {'output': history[j]['content']})
            l += 'input:' + str(max_num) + " " + history[j]['content']
            i -= 2
            max_num += 1
        
    else:
        i = 0
        j = 1
        l=""

        while j < len(history):
            mes.append({'role': "user", "content" : history[i]['content']}, {'output': history[j]['content']})
            l += 'input:' + str(j) + " " + history[j]['content']
            i += 2
            j += 2
            
    return mes,l
