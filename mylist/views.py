from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Checklist, Sublist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ChecklistForm, ItemForm, List_code_Form
#from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def start_page(request):
    return render(request, 'mylist/start_page.html', {})

@login_required
def issues_to_fix(request):
    return render(request, 'mylist/issues_to_fix.html' , {})


#u=User.objects.get(username='cdq') note - GET
#u = cdq User
#u.id = 3
#a1 = Sublist(sub_user = u) ... save user part first
#a1.save()
#p1=Checklist.objects.get(list_name='daily)
#p1.save() required
#a1.sub_list.add(p1)
#p2=Checklist.objects.get(list_name='weekly)
#p2.save() REQUIRED
#a1.sub_list.add(p2)
#a1.sub_list.all() - gives checklists for sublist
#p1.sublist_set.all() - gives sublist for checklist - nb- lower case s & no underscore
# Checklist.objects.get(list_name='weekly').sublist_set.all() ... returns Sublists
#Sublist.objects.filter(sub_list=cw) - returns <Sublist: mylist.Checklist.None ndg>, ...
#a1.sub_user - returns <User:adq>
#a1.sub_list.all() returns [] if empty - need to have .all() bc is a set
#s1=Sublist.objects.get(sub_list=18) ... s1 = <Sublist:mylist.Checklist.None stupaggio>
# clist=a1.sub_list.all()
#clist ... returns a Checklist
#cw=a1.sub_list.all()
#cw returns ... [Checklist:monday monday stup]
#cw[0] return Checklist: mond mond stup
#cw[0].list_name returns monday

#---------------
#a1.sub_list.all() - returns <Checklist:monday65 mkr= stup..>
#a1 - returns <Sublist: rg>



@login_required
def show_user_subs_list(request):
    me = request.user
    lists = Sublist.objects.filter(sub_user=me)
    return render(request, 'mylist/show_user_subs_list.html',{'Sublist':lists})

@login_required
def show_all_lists(request):
    #old version...
    #lists = Checklist.objects.all()
    #return render(request, 'mylist/show_all_lists.html',{'Checklist':lists})
    #new version...
    print ("show_all_lists VIEW processed")
    me = request.user
    lists = Checklist.objects.exclude(chklists__sub_user=me)
    return render(request, 'mylist/show_all_lists.html',{'Checklist':lists})
    
@login_required
def show_subscribers_for_all_lists(request):
    lists = Sublist.objects.all().order_by('sub_user')
    return render (request, 'mylist/show_all_sublists.html', {'Sublist':lists})
    

@login_required
def show_all_sublists(request):
    lists = Sublist.objects.all()
    return render (request, 'mylist/show_all_sublists.html', {'Sublist':lists})

#@login_required
#def show_list_items(request,pk):
#    list_items = Item.objects.filter( shoplist = pk) 
#    list_to_show = Checklist.objects.filter( id = pk)
#    return render (request, 'mylist/show_list_items.html', {'Item': list_items, 'Checklist' : list_to_show} )
    
    

@login_required
def checklist_detail(request, pk):
    #shows items in a checklist with id=pk
    checklist = get_object_or_404(Checklist, pk=pk)
    return render(request,'mylist/checklist_detail.html', {'checklist': checklist})


@login_required
def list_new(request):
    #if form is filled save data else redirect back to form
    if request.method == "POST":
        form = ChecklistForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.list_mkr = request.user
            print ("post.list_name = " , post.list_name)
            #if checklist exists with same list_name AND same list_mkr then reset form
            if checklist_list_name_exists_for_list_mkr(post.list_name, post.list_mkr) == True:
                print ("duplicate list name - resetting form")
                form = ChecklistForm()
                print ("reset form for checklist")
                return render (request, 'mylist/list_edit.html', {'form':form})
                
            else:
                print ("no duplicate list name")
                post.save()
            
            return redirect('mylist/views/show_all_lists')
            #return redirect('mylist.views.list_detail', pk=post.pk) if editing after     
    else:
        #reset blank form
        form = ChecklistForm()
        print ("reset form for checklist")
    return render (request, 'mylist/list_edit.html', {'form':form})
    

def checklist_list_name_exists_for_list_mkr(list_name, list_mkr):
    if Checklist.objects.filter(list_name=list_name).filter(list_mkr=list_mkr).exists():
        print ("checklist_list_name_for_list_mkr already exists and will return True")
        return True
    else:
        print ("checklist_list_name_for_list_mkr already exists & will return False")
        return False
        
def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

@login_required
def add_item_to_list(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.post = post
            item.save()
            return redirect ('mylist/item_edit') #('mylist.views.add_item_to_list.html', {'pk':pk})
    else:
        #reset blank form
        form = ItemForm()   
        print ("reset form for item")
    return render(request, 'mylist/item_edit.html',{'form':form})

@login_required
def add_item_to_checklist(request,pk):
    print ("post_comment_to_post VIEW processed")
    checklist = get_object_or_404(Checklist, pk=pk)
    print ('checklist.id =' , checklist.id)
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            #shoplist not in form & current checklist is saved to shoplist field
            item.shoplist = checklist 
            item.save()
            return redirect('checklist_detail', pk=checklist.pk) #return redirect('mylist.views.checklist_detail', pk=checklist.pk)
    else:
        form = ItemForm()
    return render(request, 'mylist/add_item_to_checklist.html', {'form':form})
    
    
@login_required
def item_remove(request, pk):
    #works but code needs to be tidied up
    print ("item_remove VIEW processed")
    item = get_object_or_404(Item, pk=pk)
    checklist_pk = item.shoplist
    print ('checklist_pk =' , checklist_pk.pk)
    item.delete()
    print ('checklist_pk =' , checklist_pk.pk)
    return redirect ('checklist_detail', pk=checklist_pk.pk ) #return redirect ('mylist.views.checklist_detail', pk=checklist_pk.pk )
    
@login_required
def item_purchased(request, pk):
    #works but code needs to be tidied up
    print ("item_purchased VIEW processed")
    item = get_object_or_404(Item, pk=pk)
    print ( 'prior item action =' , item.action)
    item.purchased()
    print ('item.action =' , item.action)
    return redirect ('checklist_detail', pk=item.shoplist.pk ) #return redirect ('mylist.views.checklist_detail', pk=item.shoplist.pk )

@login_required
def checklist_remove(request, pk):
    post = get_object_or_404(Checklist, pk=pk)
    post.delete()
    return redirect ('checklist_mkr')
    

#u=User.objects.get(username='cdq') note - GET
#u = cdq User
#u.id = 3
#a1 = Sublist(sub_user = u) ... save user part first
#a1.save()
#p1=Checklist.objects.get(list_name='daily)
#p1.save() required
#a1.sub_list.add(p1)
#p2=Checklist.objects.get(list_name='weekly)
#p2.save() REQUIRED
#a1.sub_list.add(p2)
#a1.sub_list.all() - gives checklists for sublist
#p1.sublist_set.all() - gives sublist for checklist - nb- lower case s & no underscore
# Checklist.objects.get(list_name='weekly').sublist_set.all() ... returns Sublists
#Sublist.objects.filter(sub_list=cw) - returns <Sublist: mylist.Checklist.None ndg>, ...
#a1.sub_user - returns <User:adq>
#a1.sub_list.all() returns [] if empty - need to have .all() bc is a set
#s1=Sublist.objects.get(sub_list=18) ... s1 = <Sublist:mylist.Checklist.None stupaggio>
# clist=a1.sub_list.all()
#clist ... returns a Checklist
#cw=a1.sub_list.all()
#cw returns ... [Checklist:monday monday stup]
#cw[0] return Checklist: mond mond stup
#cw[0].list_name returns monday
#---------------
#a1.sub_list.all() - returns <Checklist:monday65 mkr= stup..>
#a1 - returns <Sublist: rg>

#my_author_object.books.all(),

#checklist.chklist.all()

@login_required
def checklist_subd(request):
    print ("checklist_subd VIEW processed")
    me = request.user
    #need to have checklists = set of pk's with sub_user = me
    #sublists_for_user = Sublist.objects.filter(sub_user=me)
    #print ( ' subscribed lists =' , sublists_for_user.sub_list.all())
    checklists = Checklist.objects.filter(chklists__sub_user=me)
    return render(request, 'mylist/checklist_subd.html',{'checklists':checklists})
    

def check_if_user_subscribed_to_checklist(user_to_check, pk):
    #use checklist.pk to check if current user is subscribed & return Ture or False
    print ("check_if_user_subscribed_to_checklist VIEW processed")
    
    print( "user_to_check =" , user_to_check , " & checklist/sub_list pk=", pk)
    
    #if subscribed Sublist will have sub_list=checklist.pk AND sub_user=request.user.id
    if Sublist.objects.filter(sub_list=pk) and Sublist.objects.filter(sub_user=user_to_check):
        print (user_to_check, "is subscribed to checklist." , pk)
        return True
    else:
        print (user_to_check , "is NOT subscribed to checklist." , pk)
        return False

@login_required
def checklist_mkr(request):
    print ("checklist_mkr VIEW processed")
    me = request.user
    checklists = Checklist.objects.filter(list_mkr = me) #.order_by('list_name')
    return render(request, 'mylist/checklist_mkr.html', {'checklists': checklists})


def subscribe(request, pk):
    #check if user is already subscribed using current user.id and checklist.pk & returns True or False
    user_to_subscribe = request.user
    print ("subscribe function called")
    print ( "before subscribing... user_to_check = " , user_to_subscribe)
    already_subscribed = check_if_user_subscribed_to_checklist(user_to_subscribe,pk=pk)
    print ( "check returned - " , already_subscribed )
    if already_subscribed == True:
        print ( "user is ALREADY subscribed ... no further action required")
        #redirect back to subscribed lists
        return redirect('checklist_subd') #redirect('mylist.views.show_user_subs_list')
    else:
        print ("continuine to subscribing section of code...")
    
    #get User instance for given username & check it
    user_to_subscribe = request.user
    print ('subscribing - ' , user_to_subscribe )
    
    #create new sub_list entry using user instance, save tu new sublist & check it
    new_sublist_entry = Sublist (sub_user = user_to_subscribe)
    new_sublist_entry.save()
    print ("new_sublist_entry = " , new_sublist_entry, new_sublist_entry.pk)
    
    #create Checklist instance for given list_name & save & check it
    new_checklist = Checklist.objects.get(pk = pk)
    new_checklist.save()
    print ( "new_checklist = ")
    print ( new_checklist )
    
    #add Checklist to Sublist and check sublist & checklist
    new_sublist_entry.sub_list.add(new_checklist)
    print ("checklists for given sublist -")
    print ( new_sublist_entry.sub_list.all())
    #print ("sublists for given checklist -")
    #print ( new_checklist.sub_list_set.all) #old version was... new_checklist.sub_list_set.all
    
    #redirect back to subscribed lists
    return redirect('checklist_subd') 
    
    #LATER - check if already subscribed before adding a new subscription or hide subscribed link on previous page
    #LATER - add unsubscribe button to subscribed listå
    #LATER - don't add if already done
    


def is_user_subscribed(request,pk):
    #this function uses checklist.pk and prints to terminal window only
    
    print ("is_user_subscribed function called")
    user_to_check = request.user.id
    print( "user_to_check =" , user_to_check , " & checklist/sub_list pk=", pk)
    
    #if subscribed Sublist will have sub_list=checklist.pk AND sub_user=request.user.id
    if Sublist.objects.filter(sub_list=pk) and Sublist.objects.filter(sub_user=user_to_check):
        print (request.user, "is subscribed to checklist." , pk )
    else:
        print (request.user , "is NOT subscribed to checklist." , pk)
    return redirect ('show_all_lists')



def is_user_a_subscriber(request,pk):
    #returns True/False & pk required is checklist.pk which is also sub_list.pk
    print ("is_user_a_subscriber function called")
    user_to_check = request.user.id
    print( "user_to_check =" , user_to_check , " & checklist/sub_list pk=", pk)
    
    #if subscribed Sublist will have sub_list=checklist.pk AND sub_user=request.user.id
    if Sublist.objects.filter(sub_list=pk) and Sublist.objects.filter(sub_user=user_to_check):
        print (request.user, "is subscribed to checklist." , pk)
        return True
    else:
        print (request.user , "is NOT subscribed to checklist." , pk)
    return False
    
    



def un_subscribe(request, pk):
    #takes checklist.pk to unsubscribe
    #best to clear instead of removing sublists
    
    #get User instance for given username & check it
    user_to_un_subscribe = request.user
    print ('1.unsusbscribe user =' , user_to_un_subscribe )
    
    #create Checklist instance for given list_name to be deleted & print it 
    checklist_to_del = Checklist.objects.get(pk = pk)
    print ('2.checklist_to_del instance =', checklist_to_del)
    print ( '3.checklist_to_del.id =' ,  checklist_to_del.id )
    
    #create new sub_list entry using user instance, to be deleted & print it
    sublist_to_remove = Sublist.objects.filter(sub_list = checklist_to_del.id).filter(sub_user =user_to_un_subscribe) 
    print ( '4.sublist_to_clear =' , sublist_to_remove)
    print ( '4a. sublist_to_clear.all =', sublist_to_remove.all())
    
    
    print ("5.checklists for given sublist -")
    print ( sublist_to_remove[0]) #print ( sublist_to_remove.sub_list.all())
    print ("6.sublists for given checklist -")
    print ( checklist_to_del) #print ( checklist_to_del.sublist_set.all)
    
    #delete Checklist to Sublist & vise-versa then check sublist & checklist deleted
    #sublist_to_remove.sub_list.clear()
    #sublist_to_remove.sub_user = 2
    #checklist_to_del.sublist_set.clear()#clear(sublist_to_remove
    # THIS WORKED --- sublist_to_remove[0].sub_list=[]
    #this works too - sublist_to_remove[0].sub_list.clear()
    sublist_to_remove[0].sub_list.clear()
    
    
    
    print ("7.checklists for given sublist -")
    print ( sublist_to_remove) #print ( sublist_to_remove.sub_list.all())
    print ("8.sublists for given checklist -")
    print ( checklist_to_del) #print ( checklist_to_del.sublist_set.all)
    
    #redirect back to subscribed lists
    return redirect('checklist_subd')
    
def index(request):
    print ("index.html")
    return render(request, 'mylist/index.html')

def username_present(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


@login_required
def confirm_list_code(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)
    required_list_code = checklist.list_code
    print ("required_list_code =" , required_list_code)
    if request.method == "POST":
        form = List_code_Form(request.POST)
        if form.is_valid():
            list_access_code = form.save(commit=False)
            print ("list_access_code.list_code =" , list_access_code.list_code)
            if list_access_code.list_code == required_list_code:
                subscribe(request,pk=pk)
                return redirect ('checklist_subd') #('mylist.views.add_item_to_list.html', {'pk':pk})
            else:
                print ("list_code incorrect - try again")
                return redirect ('show_all_lists')
                
    else:
        #reset blank form
        form = List_code_Form()   
        print ("reset form for List_code_Form")
    return render(request, 'mylist/confirm_list_code.html',{'form':form})

#search function

@login_required
def search_for_lists(request):
    print ("search_for_lists VIEW processed")
    me = request.user
    lists = Checklist.objects.exclude(chklists__sub_user=me)
    return render(request, 'mylist/search_for_lists.html' , {'Checklist':lists})
    


