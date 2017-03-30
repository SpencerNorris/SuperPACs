from django.db import models

# Create your models here.

class Representative(models.Model):
    '''
    Representative class which represents Representatives.
    '''
    ##PROPUBLICA api id.
    propublicaid = models.CharField(max_length = 9,unique=True)

    first_name = models.CharField(max_length = 140)
    middle_name = models.CharField(max_length = 140,default="")
    last_name = models.CharField(max_length = 140)

    district = models.CharField(max_length = 140,default="0")
    state = models.CharField(max_length = 140)
    sitelink = models.CharField(max_length = 500,default="https://www.wikipedia.org/")
    #office = models.BooleanField(default=True)


    PARTIES =   (("D","Democrat"),
                ("R","Republican"),
                )
    party = models.CharField(max_length=1, choices=PARTIES)

    CHAMBERS =   (("H","House"),
                ("S","Senate"),
                )
    chamber = models.CharField(max_length=1, choices=CHAMBERS)


    ##FEC api id
    fecid = models.CharField(max_length = 9,default = "222222222")


    def __str__():
        return self.name+" ("+party+")"

    ##getters



##Can we do this subclass things?
#class Senator(models.Model):

class SuperPAC(models.Model):
    '''
    SuperPAC class which represents SuperPACs.
    '''
    name = models.CharField(max_length = 140)
    sitelink = models.CharField(max_length = 500,default="https://www.wikipedia.org/")

    ##PROPUBLICA api id reference.
    propublicaid = models.CharField(max_length = 9)

    ##FEC api id
    fecid = models.CharField(max_length = 9,default = "111111111")


    def __str__():
        return self.name


class Bill(models.Model):
    '''
    Bill class which represents Bill. Is either passed or not passed.
    '''
    name = models.CharField(max_length = 140)


    sitelink = models.CharField(max_length = 500,default="https://www.wikipedia.org/")
    hr = models.IntegerField()
    ##more details about the bill? Sponsors? co-sponsors?

    ##PROPUBLICA api id.
    propublicaid = models.CharField(max_length = 9,default = "1")

    ##FEC api id
    fecid = models.CharField(max_length = 9,default = "ccccccccc")

    def __str__():
        return self.name


class Vote(models.Model):
    '''
    Vote class which represents a Representative voting on a Bill.
    '''
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    decision = models.IntegerField()

    def __str__():
        return self.representative.__str__()+","+self.bill.__str__()+","+self.decision


class Donation(models.Model):
    '''
    Donation class that acts as a donation edge from SuperPACs to Representatives.
    '''
    superpac = models.ForeignKey(SuperPAC, on_delete=models.CASCADE)##figure out what is best here.
    represenative = models.ForeignKey(Representative, on_delete=models.CASCADE)
    amount = models.IntegerField()
    support_options =   (("S","Support"),
                        ("A","Against"),
                        )
    support = models.CharField(max_length=1, choices=support_options,default="S")
    #uniqueid = models.CharField(max_length = 40,default = "1")

    def __str__():
        return self.superpac.__str__()+","+self.representative.__str__()+","+self.amount
