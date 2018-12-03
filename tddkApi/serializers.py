from rest_framework import serializers
from .models import TypeOffre, Offre,User, Domaine

class UserSerializer(serializers.ModelSerializer):
    offres = serializers.HyperlinkedIdentityField( view_name='useroffre-list', lookup_field='username')
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'offres', )

class OffreSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

    #Permet de recuperer les champs relative au Id specifie
    auteur = serializers.StringRelatedField()
    domaine=serializers.StringRelatedField()
    typeoffre=serializers.StringRelatedField()


    def get_validation_exclusions(self):
        # Need to exclude `author` since we'll add that later based off the request
        exclusions = super(OffreSerializer, self).get_validation_exclusions()
        return exclusions + ['author']

    class Meta:
        model = Offre
        #field=('id','auteur','typeOffre','titre','jobID','description','profilRequis','avantageRelative','publishOn','dateOuverture','dateLimite','localisation')
        fields = '__all__' 

class DomaineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Domaine
        fields=('id', 'nomDomaine','descriptionDomaine')

class TypeOffreSerailizer(serializers.ModelSerializer):
      class Meta:
        model=TypeOffre
        field=('id','nomType')