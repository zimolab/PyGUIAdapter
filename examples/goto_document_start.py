from pyguiadapter import GUIAdapter


def user_function_1(a: int, b: int) -> int:
    """This is a user function.

    Below are some random sentences to mock a long document which will make the vertical scrollbar appear:

    Certainly! Here are some randomly generated sentences for testing purposes:

        The sky was filled with a myriad of twinkling stars.

        The cat crept silently through the dark alley, its eyes glinting in the moonlight.

        The children laughed and played in the park, enjoying the warm summer day.

        The bookshelf was overflowing with a diverse collection of books, ranging from fiction to non-fiction.

        The music filled the room, creating a relaxing atmosphere for the evening.

        The sun slowly rose over the horizon, painting the sky with a spectrum of colors.

        The baker carefully arranged the freshly baked pastries on the display counter.

        The scientist conducted a series of experiments to test the effectiveness of the new drug.

        The painter brushed strokes of vibrant colors onto the canvas, creating a masterpiece.

        The student diligently studied for the exam, hoping to achieve a good score.

        The river flowed gently through the valley, reflecting the surrounding landscape.

        The teacher explained the complex concept in simple terms, making it easier for the students to understand.

        The cityscape was illuminated by the neon lights, creating a futuristic atmosphere.

        The farmer harvested the ripe crops from the field, preparing for the market.

        The news report highlighted the latest developments in the political situation.

        The chef prepared a delicious meal, combining various flavors and ingredients.

        The artist captured the essence of the subject in their portrait, making it come alive on the canvas.

        The scientist observed the behavior of the animals in their natural habitat.

        The rain fell gently on the windowpane, creating a calming effect.

        The writer poured their heart out in the poem, expressing their deep emotions.

    These sentences cover a variety of topics and sentence structures, suitable for testing various aspects of language processing and understanding.

    """
    return a + b


def user_function_2(a: int, b: int) -> int:
    """This is a user function.

    Below are some random sentences to mock a long document which will make the vertical scrollbar appear:

    Certainly! Here are some randomly generated sentences for testing purposes:

        The sky was filled with a myriad of twinkling stars.

        The cat crept silently through the dark alley, its eyes glinting in the moonlight.

        The children laughed and played in the park, enjoying the warm summer day.

        The bookshelf was overflowing with a diverse collection of books, ranging from fiction to non-fiction.

        The music filled the room, creating a relaxing atmosphere for the evening.

        The sun slowly rose over the horizon, painting the sky with a spectrum of colors.

        The baker carefully arranged the freshly baked pastries on the display counter.

        The scientist conducted a series of experiments to test the effectiveness of the new drug.

        The painter brushed strokes of vibrant colors onto the canvas, creating a masterpiece.

        The student diligently studied for the exam, hoping to achieve a good score.

        The river flowed gently through the valley, reflecting the surrounding landscape.

        The teacher explained the complex concept in simple terms, making it easier for the students to understand.

        The cityscape was illuminated by the neon lights, creating a futuristic atmosphere.

        The farmer harvested the ripe crops from the field, preparing for the market.

        The news report highlighted the latest developments in the political situation.

        The chef prepared a delicious meal, combining various flavors and ingredients.

        The artist captured the essence of the subject in their portrait, making it come alive on the canvas.

        The scientist observed the behavior of the animals in their natural habitat.

        The rain fell gently on the windowpane, creating a calming effect.

        The writer poured their heart out in the poem, expressing their deep emotions.

    These sentences cover a variety of topics and sentence structures, suitable for testing various aspects of language processing and understanding.
    """
    return a + b


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(user_function_1, goto_document_start=False)
    gui_adapter.add(user_function_2, goto_document_start=True)
    gui_adapter.run()
