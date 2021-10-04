from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd

from .models import Gene;
# Create your views here.

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    return response

class Index(View):
    def get(self, request):
        get_dict = dict(request.GET)
        genes = Gene.objects.all()
        flag = False
        if get_dict:
            start = get_dict['chromosome_start'][0]
            end = get_dict['chromosome_end'][0]
            af_cutoff = get_dict['af_cutoff'][0]
            if ((start and end) and (int(start) > int(end))):
                flag = True
                messages.warning(request, 'Chromosome start cannot be greater than chromosome end')
            if (af_cutoff and float(af_cutoff) > 1):
                flag = True
                messages.warning(request, 'AF Cutoff cannot be greater than 1')                
        if not flag:
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
        values = Gene.objects.order_by('gene').values_list('gene').distinct()
        values = map(lambda x: x[0], values)
        return render(request, 'vidium/index.html', context = { 'genes' : genes, 'values': values })

    def sort(request, key, order):
        if (order == 'DESC'):
            key = '-' + key
            gene = Gene.objects.order_by(key.lower())
        else:
            gene = Gene.objects.order_by(key,lower())
        return render(request, 'vidium/index.html', context = { 'genes' : gene})

class Upload(View):
    """
    Implementing upload file to populate the table
    """

    def process_file(datafile):
        try:
            df = pd.read_excel(datafile, na_values=['None'])
        except UnicodeDecodeError:
            df = pd.read_csv(datfile)
        df_dict = df.to_dict('index')
        for item in df_dict.items():
            gene_dict = item[1]
            gene = Gene.objects.create(chrom=gene_dict['CHROM'], pos=gene_dict['POS'], ref=gene_dict['REF'], filter=gene_dict['FILTER'], alt=gene_dict['ALT'], af=gene_dict['AF'], vf=gene_dict['VF'], dp=gene_dict['DP'], allele=gene_dict['ALLELE'], effect=gene_dict['EFFECT'], impact=gene_dict['IMPACT'], gene=gene_dict['GENE'])
        gene_values = Gene.objects.values('gene').distinct()
        return gene_values
        
    def upload(request):
        if not request.FILES:
            messages.warning(request, 'Please select a file to upload!')
        else: 
            datafile = request.FILES['file']
            values = Upload.process_file(datafile)
        return redirect('vidium:index')