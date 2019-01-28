class TemplateMixin(object):

    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
        3: 'skip',
    }

    DEFAULT_TITLE = ''
    DEFAULT_TITLE_en = 'Test Results'
    DEFAULT_DESCRIPTION = ''
    DEFAULT_DESCRIPTION_en = 'Test Description'

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <title>{title}</title>
  <meta name="generator" content="{generator}" />
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> {stylesheet}
  <script language="javascript" type="text/javascript">{js}</script>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

</head>

<body onload="load();showCase(0)">
  <div id="wrapper" class="lang-en">

    
    {heading} 
    <div class="col-md-6" id="piechart"></div>
    <div class="col-md-6" id="lang">
      <ul>
        <li>
          <div href="#en" id="lang-en" title="English"></div>
        </li>
      </ul>
    </div>
    {report} {ending}
    <div id="popup">
      <div class="bg">
        <img src="" alt="" />
      </div>
    </div>
  </div>
</body>

</html>
"""

    JS = r"""
output_list = Array();
function showCase(level) {
  trs = document.getElementsByTagName("tr");
  for (var i = 0; i < trs.length; i++) {
    tr = trs[i];
    id = tr.id;
    if (id.substr(0, 2) === "st") {
      if (level === 4 || level === 3) {
        tr.className = "";
      } else {
        tr.className = "hiddenRow";
      }
    }
    if (id.substr(0, 2) === "ft") {
      if (level === 4 || level === 2) {
        tr.className = "";
      } else {
        tr.className = "hiddenRow";
      }
    }
    if (id.substr(0, 2) === "pt") {
      if (level === 4 || level === 1) {
        tr.className = "";
      } else {
        tr.className = "hiddenRow";
      }
    }
    if (id.substr(0, 2) === "et") {
      if (level === 4 || level === 5 || level === 2) {
        tr.className = "";
      } else {
        tr.className = "hiddenRow";
      }
    }
    if (id.substr(0, 4) === "div_") { tr.className = "hiddenRow"; }
  }
}

function showClassDetail(cid, count) {
  var id_list = Array(count);
  var toHide = 1;
  for (var i = 0; i < count; i++) {
    tid0 = "t" + cid.substr(1) + "." + (i + 1);
    tid = "f" + tid0;
    tr = document.getElementById(tid);
    if (!tr) {
      tid = "p" + tid0;
      tr = document.getElementById(tid);
      if (!tr) {
        tid = "e" + tid0;
        tr = document.getElementById(tid);
        if (tr === null) {
          tid = "s" + tid0;
          tr = document.getElementById(tid);
        }
      }
    }
    id_list[i] = tid;
    if (tr.className) {
      toHide = 0;
    }
  }
  for (var i = 0; i < count; i++) {
    tid = id_list[i];
    if (toHide && tid.indexOf("p") !== -1) {
      document.getElementById(tid).className = "hiddenRow";
    } else {
      document.getElementById(tid).className = "";
    }
    document.getElementById("div_" + tid).className = "hiddenRow";
  }
}

function showTestDetail(div_id) {
  var details_div = document.getElementById(div_id);
  var className = details_div.className;
  if (className != "") {
    details_div.className = "";
  } else {
    details_div.className = "hiddenRow";
  }
}

function html_escape(s) {
  s = s.replace(/&/g, "&amp;");
  s = s.replace(/</g, "&lt;");
  s = s.replace(/>/g, "&gt;");
  return s;
}

function load() {
  var el_wrapper = document.getElementById('wrapper');
  document.getElementById('lang-en').onclick = function () { el_wrapper.className = 'lang-en'; };

  var h = (location.hash || '').replace(/#/, '');
  var nav_lang;
  el_wrapper.className = 'lang-en' + h;

  var imgs = document.getElementsByClassName("pic");
  var lens = imgs.length;
  var popup = document.getElementById("popup");
  for (var i = 0; i < lens; i++) {
    imgs[i].onclick = function (event) {
      event = event || window.event;
      var target = document.elementFromPoint(event.clientX, event.clientY);
      showBig(target.src);
    };
  }
  popup.onclick = function () {
    popup.getElementsByTagName("img")[0].src = "";
    popup.style.display = "none";
    popup.style.zIndex = "-1";
  };
  function showBig(src) {
    popup.getElementsByTagName("img")[0].src = src;
    popup.style.display = "block";
    popup.style.zIndex = "999999";
  }
  google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);
    
    // Draw the chart and set the chart values
    function drawChart() {
      var data = google.visualization.arrayToDataTable([
      ['Status', 'Status'],
      ['Failed', %(fail)d],
      ['Passed', %(Pass)d],
      ['Skip', %(skip)d],
      ['Error', %(error)d],
    
    ]);
    
      // Optional; add a title and set the width and height of the chart
      var options = {'title':'Status', 'width':400, 'height':300, colors: ['#D8000C', '#4BB543', '#F1C40F', '#17202A'],};
    
      // Display the chart inside the <div> element with id="piechart"
      var chart = new google.visualization.PieChart(document.getElementById('piechart'));
      chart.draw(data, options);
    }
}
    
"""

    STYLESHEET_TMPL = r"""<style type="text/css" media="screen">
  body {
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 14px;
  }

  pre {
    word-wrap: break-word;
    word-break: break-all;
    overflow: auto;
    white-space: pre-wrap
  }

  h1 {
    font-size: 16pt;
    color: gray
  }

  a.popup_link:hover {
    color: red
  }

  .popup_window {
    display: block;
    position: relative;
    left: 0;
    top: 0;
    padding: 10px;
    background-color: #E6E6D6;
    text-align: left;
    font-size: 13px
  }

  #result_table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid #777
  }

  #header_row {
    color: #fff;
    background-color: #777
  }

  #result_table td {
    border: 1px solid #777;
    padding: 2px;
    min-width: 70px;
    width: 100%
  }

  #result_table td:nth-child(n+2) {
    text-align: center
  }

  #total_row {
    font-weight: bold
  }

  .passClass,
  .failClass,
  .errorClass,
  .skipClass {
    font-weight: bold
  }

  .passCase {
    background-color: #97cc64
  }

  .failCase {
    background-color: #fd5a3e
  }

  .errorCase {
    background-color: #ffd050
  }

  .skipCase {
    background-color: #aaa
  }

  .hiddenRow {
    display: none
  }

  .testcase {
    margin-left: 2em
  }

  #popup {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    text-align: center;
    display: none
  }

  #popup .bg {
    background-color: rgba(0, 0, 0, .5);
    width: 100%;
    height: 100%
  }

  @media \0screen\,screen\9 {
    #popup .bg {
      background-color: #000;
      filter: Alpha(opacity=50);
      position: static
    }
    #popup .bg img {
      position: relative
    }
  }

  #popup img {
    max-width: 100%;
    max-height: 100%;
    margin: auto;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
  }

  img.pic {
    width: 500px;
    cursor: pointer;
  }

  #wrapper {
    margin: 0 auto;
    border-top: solid 2px;
  }
  
  #wrapper.lang-en p.lang-en {
  }

  #wrapper.lang-en span.lang-en {
  }

  #lang ul {
    float: right;
    margin: 0;
    padding: 2px 10px 4px 10px;
    border-radius: 0 0 4px 4px;
    list-style: none;
  }

  #lang li {
    margin: 0;
    float: left;
    padding: 0 5px;
  }

  #lang li a {
    display: block;
    width: 24px;
    height: 24px;
    text-indent: -4em;
    overflow: hidden;
  }
</style>"""

    HEADING_TMPL = r"""<div class='heading col-md-12'>
  <h1>{title}</h1>
  <p class='attribute'>
    <strong>
      <span class="lang-en">Start Time:</span>
    </strong> {startTime}
  </p>
  <p class='attribute'>
    <strong>
      <span class="lang-en">End Time:</span>
    </strong> {endTime}
  </p>
  <p class='attribute'>
    <strong>
      <span class="lang-en">Duration:</span>
    </strong> {duration}
  </p>
  <p class='attribute'>
    <strong>
      <span class="lang-en">Status:</span>
    </strong>
    <span class="lang-en">Total:</span>{total}&nbsp;&nbsp;&nbsp;&nbsp;
    <span class="lang-en">Passed:</span>{Pass}&nbsp;&nbsp;&nbsp;&nbsp;
    <span class="lang-en">Failed:</span>{fail}&nbsp;&nbsp;&nbsp;&nbsp;
    <span class="lang-en">Error:</span>{error}&nbsp;&nbsp;&nbsp;&nbsp;
    <span class="lang-en">Skipped:</span>{skip}&nbsp;&nbsp;&nbsp;&nbsp;
  </p>
</div>"""

    REPORT_TMPL = r"""<br\>
<p id='show_detail_line'>
    Show:
    </br>
    <input type="radio" name = "1" value="1" onclick = "showCase(0)"/>
        <label for="1">
            
                <span class="lang-en">Summary</span>
            
        </label>
    <br/>
    <input type="radio" name = "1" value="1" onclick = "showCase(1)"/>
        <label for="1">
            <span class="lang-en">Pass</span>         
        </label>
    <br/>
    <input type="radio" name = "1" value="1" onclick = "showCase(2)"/>
        <label for="1">
                <span class="lang-en">Fail</span>
        </label>
    <br/>
    <input type="radio" name = "1" value="1" onclick = "showCase(5)"/>
        <label for="1">
                <span class="lang-en">Error</span>
        </label>
    <br/>
    <input type="radio" name = "1" value="1" onclick = "showCase(3)"/>
        <label for="1">
                <span class="lang-en">Skip</span>
        </label>
    <br/>
    <input type="radio" name = "1" value="1" onclick = "showCase(4)"/>
        <label for="1">
                <span class="lang-en">ALL</span>
        </label>
</p>
<table id='result_table'>
  <tr id='header_row'>
    <th>
      <span class="lang-en">Test Group/Test case</span>
    </th>
    <th>
      <span class="lang-en">Count</span>
    </th>
    <th>
      <span class="lang-en">Passed</span>
    </th>
    <th>
      <span class="lang-en">Failed</span>
    </th>
    <th>
      <span class="lang-en">Erroneous</span>
    </th>
    <th>
      <span class="lang-en">Skipped</span>
    </th>
    <th>
      <span class="lang-en">Statistics</span>
    </th>
    <th>
      <span class="lang-en">View</span>
    </th>
  </tr>
  {test_list}
  <tr id='total_row'>
    <td>
    <span class="lang-en">Total</span>
    </td>
    <td>{count}</td>
    <td class="passCase">{Pass}</td>
    <td class="failCase">{fail}</td>
    <td class="errorCase">{error}</td>
    <td class="skipCase">{skip}</td>
    <td style="text-align:right;">{statistics:.2%}</td>
    <td>&nbsp;</td>
  </tr>
</table>
"""

    REPORT_CLASS_TMPL = r"""
<tr class='{style}'>
  <td>{desc}</td>
  <td>{count}</td>
  <td class="passCase">{Pass}</td>
  <td class="failCase">{fail}</td>
  <td class="errorCase">{error}</td>
  <td class="skipCase">{skip}</td>
  <td style="text-align:right;">{statistics:.2%}</td>
  <td>
    <a href="javascript:showClassDetail('{cid}',{count})">
      <span class="lang-en">Detail</span>
    </a>
  </td>
</tr>
"""

    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='{tid}' class='{Class}'>
  <td class='{style}'  colspan='7'>
    <div class='testcase'><b>{test_name}</b> {desc}</div>
  </td>
  <td class='{style}' align='center'>
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_{tid}')">{status}</a>
  </td>
</tr>
<tr id='div_{tid}' class="hiddenRow">
  <td colspan='8'>
    <div class="popup_window">
      <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_{tid}').className = 'hiddenRow' ">[x]</a>
      </div>
      <pre>{script}</pre>
      <div>{img}</div>
    </div>
  </td>
</tr>
"""

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='{tid}' class='{Class}'>
  <td class='{style}'  colspan='7'>
    <div class='testcase'><b>{test_name}</b> - {desc} </div>
  </td>
  <td class='{style}' align='center'>{status}</td>
</tr>
"""

    REPORT_TEST_OUTPUT_TMPL = r"""
{id}: 
{output}
"""

    ENDING_TMPL = r"""<div id='ending'>&nbsp;</div>"""

    REPORT_LOG_FILE_TMPL = r"""
<a href='{log_file}'>
  <span class="lang-en">Download log file</span>
</a>
"""

    REPORT_IMG_TMPL = r"""
<img class="pic" src='{img_src}' alt='{alt}' title='{alt}' />
"""
