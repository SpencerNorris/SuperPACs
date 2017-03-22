from django.db import models

# Create your models here.

class Representative(models.Model):
    '''
    Representative class which represents Representatives.
    '''

    name = models.CharField(max_length = 140)
    district = models.CharField(max_length = 140)
    state = models.CharField(max_length = 140)
    link = models.CharField(max_length = 500)

    PARTIES = (("D","Democrat"),
            ("R","Republican"),
            )
    party = models.CharField(max_length=1, choices=PARTIES)

    def __str__():
        return self.name+" ("+party+")"

##Can we do this subclass things?
#class Senator(models.Model):

class SuperPAC(models.Model):
    '''
    SuperPAC class which represents SuperPACs.
    '''
    name = models.CharField(max_length = 140)
    link = models.CharField(max_length = 500)


    def __str__():
        return self.name


class Legislation(models.Model):
    '''
    Legislation class which represents Legislation.
    '''
    name = models.CharField(max_length = 140)
    hr = models.IntegerField()
    link = models.CharField(max_length = 500)
    ##more details about the bill? Sponsors? co-sponsors?

    def __str__():
        return self.name


class Vote(models.Model):
    '''
    Vote class which represents a Representative voting on Legislation.
    '''
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE)
    legislation = models.ForeignKey(Legislation, on_delete=models.CASCADE)
    decision = models.IntegerField()

    def __str__():
        return self.representative.__str__()+","+self.legislation.__str__()+","+self.decision


class Donation(models.Model):
    '''
    Donation class that acts as a donation edge from SuperPACs to Representatives.
    '''
    superpac = models.ForeignKey(SuperPAC, on_delete=models.CASCADE)##figure out what is best here.
    represenative = models.ForeignKey(Representative, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__():
        return self.superpac.__str__()+","+self.representative.__str__()+","+self.amount
