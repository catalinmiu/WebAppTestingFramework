from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import subprocess
import os
import random
import datetime
from subprocess import Popen, PIPE
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'app/index.html')