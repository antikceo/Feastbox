from haystack import indexes
from dishes.models import Dishes


class DishesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='name')
    ingredients = indexes.CharField(model_attr='ingredients')
	
    def get_model(self):
        return Dishes
        
	def index_queryset(self):
		return self.get_model().objects.all()