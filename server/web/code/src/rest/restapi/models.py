from django.db import models

# Create your models here.
'''
Representative class which represents Representatives.
'''
class Representative(models.Model):
    name = models.charField(max_length = 140)
    district = models.charField(max_length = 140)
    state = models.charField(max_length = 140)
    PARTIES = (("D":"Democrat"),
            ("R":"Republican"),
            )
    party = models.CharField(max_length=1, choices=PARTIES)


    def __str__():
        return self.name+" ("+party+")"

##Can we do this subclass things?
#class Senator(models.Model):
'''
SuperPAC class which represents SuperPACs.
'''
class SuperPAC(models.Model):
    name = models.charField(max_length = 140)

    def __str__():
        return self.name

'''
Legislation class which represents Legislation.
'''
class Legislation(models.Model):
    name = models.charField(max_length = 140)
    hr = models.IntegerField()
    ##more details about the bill? Sponsors? co-sponsors?

    def __str__():
        return self.name

'''
Vote class which represents a Representative voting on Legislation.
'''
class Vote(models.Model):
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE)
    legislation = models.ForeignKey(Legislation, on_delete=models.CASCADE)
    decision = models.IntegerField()

    def __str__():
        return self.representative.__str__()+","+self.legislation.__str__()+","+self.decision
'''
Donation class that acts as a donation edge from SuperPACs to Representatives.
'''
class Donation(models.Model):
    superpac = models.ForeignKey(SuperPAC, on_delete=models.CASCADE)##figure out what is best here.
    represenative = models.ForeignKey(Representative, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__():
        return self.superpac.__str__()+","+self.representative.__str__()+","+self.amount
