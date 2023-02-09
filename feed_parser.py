import feedparser


# Initializing variables
required_fields = {'id': 'g_id', 
                   'title': 'g_title', 
                   'link': 'link', 
                   'product_type': 'g_product_type', 
                   'image_link': 'g_image_link', 
                   'availability': 'g_availability', 
                   'price': 'g_price'}
error = {}
categories = {}
unique_available_prodacts = {}

# Checking field existence
def field_exists(new_item, field):
    if not new_item.get(required_fields[field], None):
        return False
    return True

# Parsing Google feed file
def feeds_parser(file_url):
    return feedparser.parse(file_url)


def get_headlines(file_url):
    feed = feeds_parser(file_url)
    for new_item in feed['items']:
        id = new_item[required_fields['id']]
        title = new_item.get(required_fields['title'], None)

        missing_fields = []

        if not title:
            title_key = f'No title, id is {id}'
            missing_fields.append('title')
        else:
            title_key = f'Title is "{title}", id is {id}'

        for item in list(required_fields.keys())[2:]:
            if not field_exists(new_item, item):
                missing_fields.append(item)

        if missing_fields:
            error[title_key] = missing_fields

        product_type = new_item.get(required_fields['product_type'], None)
        availability = new_item.get(required_fields['availability'], None)
        item_group_id = new_item.get('g_item_group_id', None)

        if product_type and availability == 'in_stock':
            if product_type not in categories:
                categories[product_type] = [item_group_id]
            else:
                if item_group_id not in categories[product_type]:
                    categories[product_type].append(item_group_id)
            unique_available_prodacts[product_type] = len(categories[product_type])

    return error, unique_available_prodacts


# Google Feed format files url
urls = {
    'google_feed': 'feed.xml'
}


for _, file_url in urls.items():
    # Task 1 results you can find in 'error' variable
    # Task 2 results you can find in 'unique_available_prodacts' variable
    error, unique_available_prodacts = get_headlines(file_url)
    print(error)
    print("*"*30)
    print(unique_available_prodacts)
