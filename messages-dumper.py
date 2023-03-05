import vk_api
import time

ACCESS_TOKEN = ''  # вставьте сюда свой access token
OUTPUT_FILE = 'messages.txt'  # название файла, в который занесутся полученные данные
ENCODING = 'utf-8'
LAST_NAME = ''  # Вставьте сюда свою фамилию, чтобы не учитывать сохраненные сообщения и беседы


def get_num_of_messages(peer_id: int) -> dict:
    """
    Получает общее количество сообщений в диалоге
    :param peer_id:
    :return:
    """
    return api.messages.getHistory(peer_id=peer_id, count=1, rev=0, extended=1)['items'][0]['conversation_message_id']


def get_dialog_member_name(peer_id: int) -> dict | None:
    """
    Получает имя собеседника
    :param peer_id:
    :return:
    """
    profiles = api.messages.getConversationMembers(peer_id=peer_id)['profiles']
    if len(profiles) == 1:
        return profiles[0]['first_name'] + " " + profiles[0]['last_name']
    if len(profiles) > 2:
        return None
    if profiles[0]['last_name'] == LAST_NAME:
        return profiles[1]['first_name'] + " " + profiles[1]['last_name']
    return profiles[0]['first_name'] + " " + profiles[0]['last_name']


def get_history(peer_id: int) -> dict:
    """
    Получает все сообщения в диалоге (peer_id)
    """
    params = {
        'peer_id': peer_id
    }
    for item in tools.get_all_slow_iter('messages.getHistory', 200, params):
        yield item


def get_num_per_last_year(peer_id: int) -> int:
    """
    Получает все сообщения в диалоге за последний год (peer_id)
    """
    cnt = 0

    for message in get_history(peer_id):
        if message['date'] > time.time() - 31556926:
            cnt += 1
        # time.sleep(0.5)
    return cnt


def get_dialogs() -> dict:
    """
    Получает все диалоги текущего пользователя
    :return:
    """
    for item in tools.get_all_iter('messages.getConversations', 200):
        yield item['conversation']['peer']['id']


if __name__ == '__main__':
    session = vk_api.VkApi(token=ACCESS_TOKEN)
    tools = vk_api.VkTools(session)
    api = session.get_api()

    print('Load dialogs...')

    with open(OUTPUT_FILE, 'w', encoding=ENCODING) as f:
        f.write("Name Surname Num_of_messages Per_last_year ")
        f.write('\n')
        for peer_id in get_dialogs():
            try:
                member_name = get_dialog_member_name(peer_id)
                print(f'Load info about {member_name}...')

                if member_name is None:
                    continue
                f.write(f"{member_name} {get_num_of_messages(peer_id)} {get_num_per_last_year(peer_id)}")
                f.write('\n')

                time.sleep(0.5)
            except Exception:
                continue
