from django.db import models

# Create your models here.
class RegCon(models.Model):
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=20)
    # JSONField to store monthly sales count data, allowing null values
    monthly_sales_count_blob = models.JSONField(null=True)
    # JSONField to store monthly median sales price data, allowing null values
    monthly_median_sales_price_blob = models.JSONField(null=True)
    # JSONField to store monthly median sales price per square foot data, allowing null values
    monthly_median_sales_price_persqft_blob = models.JSONField(null=True)
    # JSONField to store monthly mean sales price data, allowing null values
    monthly_mean_sales_price_blob = models.JSONField(null=True)

    class Meta:
        # Define unique constraint to ensure each combination of city and state is unique
        unique_together = ('city', 'state')