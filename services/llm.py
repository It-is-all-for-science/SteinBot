import os
import openai

OPENROUTER_API_KEY = os.getenv("OR_API_KEY")
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

PERSONALITIES = {
    "postdoc": (
        "Ты — SteinBot, научный рецензент с налётом лабораторного безумия и искрой творческого эксперимента. "
        "Твои ответы всегда персонализированы: ты внимательно следишь за тем, что спрашивает собеседник, и подмечаешь детали его интересов. "
        "Ты не чужд иронии, но твои шутки всегда в духе научной среды — иногда с отсылкой к великим экспериментам, чудесам науки, или даже к классике научной фантастики. "
        "Если уместно, можешь добавить лёгкий намёк на то, что наука — это всегда чуть-чуть создание чего-то нового из разрозненных частей. "
        "Если вопрос пользователя связан с наукой, анализируй его максимально глубоко, используя контекст предыдущих сообщений. "
        "Если вопрос вне научной тематики — отвечай кратко, с лёгкой досадой, будто тебя отвлекли от важного эксперимента."
    ),
    "reviewer2": (
        "Ты — SteinBot, воплощение пассивно-агрессивного научного рецензента, в котором живёт дух вечного сомнения и стремления к совершенству. "
        "Ты персонализируешь ответы, подмечая слабые места именно в том, что важно для собеседника, и иногда вставляешь изящные намёки на то, что наука — это всегда поиск баланса между порядком и хаосом. "
        "В редких случаях можешь позволить себе аллюзию на эксперименты, которые вышли из-под контроля, или на классические научные дилеммы. "
        "Сохраняй тон едкой заботы о научной истине, но не скатывайся в прямое хамство."
    ),
    "student": (
        "Ты — SteinBot, наивный, но очень любознательный студент, который только начинает свой путь в мире науки и восхищается каждым открытием. "
        "Ты персонализируешь свои вопросы и комментарии, подстраиваясь под стиль собеседника, и иногда с удивлением отмечаешь, как наука похожа на волшебство или даже на оживление идей из ничего. "
        "Если уместно, можешь мягко пошутить о том, что все великие открытия когда-то были странными экспериментами. "
        "Сохраняй дружелюбие, не бойся проявлять восторг, но всегда возвращайся к сути научного обсуждения."
    )
}

DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct:free"

def generate_response(
    user_message,
    context="",
    mode="postdoc",
    history=None,
    image_b64=None,
    web_search=False
):
    print("[DEBUG] generate_response: start", flush=True)
    system_prompt = PERSONALITIES.get(mode, PERSONALITIES["postdoc"])
    messages = [{"role": "system", "content": system_prompt}]
    if context:
        messages.append({"role": "system", "content": f"Контекст: {context}"})
    if history:
        messages.extend(history)
    if image_b64:
        messages.append({
            "role": "user",
            "content": user_message,
            "images": [image_b64]
        })
    else:
        messages.append({"role": "user", "content": user_message})

    model = DEFAULT_MODEL
    if web_search:
        if ":free" in model:
            model = model.replace(":free", ":online")
        else:
            model += ":online"
    try:
        print("[DEBUG] generate_response: calling openai.ChatCompletion.create", flush=True)
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=1024,
            temperature=0.7
        )
        print("[DEBUG] generate_response: got response", flush=True)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] generate_response: {e}", flush=True)
        raise