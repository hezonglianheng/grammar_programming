from django.shortcuts import render
from show.models import ReplacePair, SentencePair
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

PAGE_SIZE = 10 # 每页显示数据条数

def show_rp_pairs(request):
    replace_pairs = ReplacePair.objects.all()
    return render(request, 'show/rp_pair.html', {'replace_pairs': replace_pairs})

def show_sentences(request, rp_pair: str):
    sentences = SentencePair.objects.filter(rp_pair__rp_pair=rp_pair)
    paginator = Paginator(sentences, PAGE_SIZE)

    try:
        page = request.GET.get('page')
        page = int(page)
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = paginator.num_pages
    except TypeError:
        page = 1
    
    page_sentences = paginator.get_page(page)
    page_start = PAGE_SIZE * (page - 1) + 1
    page_end = PAGE_SIZE * page if page * PAGE_SIZE < len(sentences) else len(sentences)
    return render(request, 'show/sentence_pair.html', {'sentences': page_sentences, 'rp_pair': rp_pair, 'sum': len(sentences), 'page_start': page_start, 'page_end': page_end, 'page': page, 'page_sum': paginator.num_pages})
