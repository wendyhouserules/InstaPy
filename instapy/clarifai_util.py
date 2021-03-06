"""Module which handles the clarifai api and checks
the image for invalid content"""
from clarifai.rest import ClarifaiApp, Image as ClImage


def check_image(browser, clarifai_api_key, img_tags, full_match=False):
    """Uses the link to the image to check for invalid content in the image"""
    clarifai_api = ClarifaiApp(api_key=clarifai_api_key)

    img_link = get_imagelink(browser)
    # Uses Clarifai's v2 API
    model = clarifai_api.models.get('general-v1.3')
    image = ClImage(url=img_link)
    result = model.predict([image])
    clarifai_tags = [concept.get('name').lower() for concept in result[
        'outputs'][0]['data']['concepts']]

    for (tags, should_comment, comments) in img_tags:
        if should_comment:
            if given_tags_in_result(tags, clarifai_tags, full_match):
                return True, comments
        else:
            if given_tags_in_result(tags, clarifai_tags, full_match):
                print('Inappropriate content in Image, not commenting')
                return False, []

    return True, []


def given_tags_in_result(search_tags, clarifai_tags, full_match=False):
    """Checks the clarifai tags if it contains one (or all) search tags """
    if full_match:
        return all([tag in clarifai_tags for tag in search_tags])
    else:
        return any((tag in clarifai_tags for tag in search_tags))


def get_imagelink(browser):
    """Gets the imagelink from the given webpage open in the browser"""
    return browser.find_element_by_xpath('//img[@class = "_2di5p"]') \
        .get_attribute('src')
