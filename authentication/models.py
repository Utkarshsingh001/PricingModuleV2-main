from django.db import models

class Pricing_Module(models.Model):
    mod_id = models.AutoField(primary_key=True)
    dbp_price = models.FloatField()
    dbp_km = models.FloatField(default=True)
    dap = models.FloatField()
    waiting_charge = models.FloatField()
    waiting_time = models.FloatField()
    status = models.BooleanField()
    usermodifiedby = models.CharField(max_length=20)
    created_at = models.DateTimeField(editable=True,auto_now_add=True)

    def str(self):
        return self

class Week_Table(models.Model):
    mod_id = models.ForeignKey(Pricing_Module, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.mod_id} {self.weekday}"

class TMF(models.Model):
    mod_id = models.ForeignKey(Pricing_Module, on_delete=models.CASCADE)
    hour = models.IntegerField()
    factor = models.FloatField()

    def __str__(self):
        return f"{self.mod_id} {self.hour} {self.factor}"

