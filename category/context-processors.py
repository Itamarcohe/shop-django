from .models import Category

# we will do the same like this just in react

# something like after getting all the data of menu links by using axios(fetch)
# we will map over the categories and will make our drop down list that user
# select a specific category


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


# for this we will create a function
# and then while mapping we will do like

# <a href="Our function that will get the url of the specific slug name">  {category.category_name }<a>

#the function is in Category model