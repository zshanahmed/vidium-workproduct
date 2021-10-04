from django.shortcuts import render, redirect
from django.core import serializers
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
import pdb

from .models import Gene;
# Create your views here.

def getValues():
    genes = Gene.objects.all()
    values = genes.values_list('gene').distinct()
    values = map(lambda x: x[0], values)
    return values

def getResults(get_dict):
    genes = Gene.objects.all()
    for key, value in get_dict.items():
        value = value[0]
        if value:
            if key == "chromosome_start":
                genes = genes.filter(pos__gte=value)
            elif key == "chromosome_end":
                genes = genes.filter(pos__lte=value)
            elif key == "af_cutoff":
                genes = genes.filter(af__lte=float(value))
            elif key == 'chromosome_id':
                genes = genes.filter(chrom=value)
            elif key == 'gene':
                if value != ('Select the gene name'):
                    genes = genes.filter(gene=value)
    return genes

class Index(View):

    def get(self, request):
        """
        Method to display the information on dashboard
        """
        try: # Clear stored metadata of filters when on dashboard
            del request.session['filters']
        except KeyError:
            pass
        genes = Gene.objects.all()
        values = getValues() # Gets values to display in options
        return render(request, 'vidium/index.html', context = { 'genes' : genes, 'values': values })

    def post(self, request):
        """
        Processing request on search
        """
        genes = Gene.objects.all()
        get_dict = dict(request.POST) 
        flag = False
        if get_dict:
            start = get_dict['chromosome_start'][0]
            end = get_dict['chromosome_end'][0]
            af_cutoff = get_dict['af_cutoff'][0]
            if ((start and end) and (int(start) > int(end))): # Chromosome position validation check
                flag = True
                messages.warning(request, 'Chromosome start cannot be greater than chromosome end')
            if (af_cutoff and float(af_cutoff) > 1): # AF Cutoff validation
                flag = True
                messages.warning(request, 'AF Cutoff cannot be greater than 1')     
            request.session['filters'] = get_dict # Setting filters information for reference in sort       
        if not flag:
            genes = getResults(get_dict)
        values = getValues()
        return render(request, 'vidium/index.html', context = { 'genes' : genes, 'values': values })

    def sort(request, key, order):
        """
        Sorts based on the required key and order
        """
        filters = request.session.get('filters') # Getting filters if there are any set right now
        if filters:
            genes = getResults(filters)
        else:
            genes = Gene.objects.all()
        if (order == 'DESC'):
            key = '-' + key
            gene = genes.order_by(key.lower())
        else:
            gene = genes.order_by(key.lower())
        values = getValues() 
        return render(request, 'vidium/index.html', context = { 'genes' : gene, 'values': values})

class Upload(View):
    """
    Uploads file to populate table 
    """

    def process_file(datafile):
        """
        Takes the Excel file and processes it 
        """
        try:
            df = pd.read_excel(datafile, na_values=['None']) # For xlsx format
        except UnicodeDecodeError:
            df = pd.read_csv(datfile) # For csv format
        df_dict = df.to_dict('index')
        for item in df_dict.items(): # Going through dict from file
            gene_dict = item[1]
            gene = Gene.objects.create(chrom=gene_dict['CHROM'], pos=gene_dict['POS'], ref=gene_dict['REF'], filter=gene_dict['FILTER'], alt=gene_dict['ALT'], af=gene_dict['AF'], vf=gene_dict['VF'], dp=gene_dict['DP'], allele=gene_dict['ALLELE'], effect=gene_dict['EFFECT'], impact=gene_dict['IMPACT'], gene=gene_dict['GENE']) # Adding entries in database
        gene_values = Gene.objects.values('gene').distinct()
        return gene_values
        
    def upload(request):
        if not request.FILES:
            messages.warning(request, 'Please select a file to upload!')
        else: 
            datafile = request.FILES['file'] # Getting file if uploaded
            values = Upload.process_file(datafile)
        return redirect('vidium:index')