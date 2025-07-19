import json
from openai import OpenAI, Client

client = OpenAI(api_key="xyu")

msg = (
    "вот столько. ну ты видишь что 2500 и 250. и чтобы мой сайт хорошо контактировал с аллегро надо взять и как то их загрупировать"
    + "как выглядит процесс. я создаю продукт (автозапчасть). она создается, далее я беру и по специальной таблице посоставимостей (которую мы сча делать будет) используя наши id, получаю id аллегро и далее посшу через api"
    "наша задача - сгупировать все так, чтобы все работало корректно. желательно o(1). в виде название запчасти :аллегро-id"
    + "чтобы не было у тя перегрузок я буду скидывать частями по 50 штук"
    + "уточнения:я тебе даю 50 имен автозапчастей, а ты просто берешь и вставляешь allegro id на то что больше подходит."
    + "пример:Блок управления FEM: 3393, Блок управления FFC: 2584,Блок управления HSR: 2270, и тдтп"
    + "я тебе даю эти данные. на ответе ты мне даешь Блок управления BSD: 4145,Блок управления CAS: 4145"
    + "все данные ты берешь из таблицы которую я буду тебе скидывать каждый раз когда буду присылать тебе порцию"
)

with open(
    "app/apis/idriver/JSON/idriver_car_parts.json",
    "r",
    encoding="utf-8",
) as file:
    loaded_data = json.load(file)
print(loaded_data.keys())

data = {}
with open("ngg.json", "a", encoding="utf-8") as file:
    for i, v in loaded_data.items():
        data.update({i: "надо выставить"})

    json.dump(data, file, ensure_ascii=False, indent=4)

# response = client.responses.create(
#     model="gpt-4.1",
#     instructions="Будь четким аналитиком в мире автозапчастей. ",
#     input=msg,
# )

# with Client(api_key=api_key) as client:
#     response = client.responses.create(
#         model="gpt-4.1-mini",
#         instructions="Будь четким аналитиком в мире автозапчастей. ",
#         input="Скажи привет",
#     )

#     print(response.output_text)
