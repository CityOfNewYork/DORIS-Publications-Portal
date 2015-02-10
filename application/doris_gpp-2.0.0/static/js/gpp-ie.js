$(document).keypress(function(e) {
    if (e.which == 13 && navigator.userAgent.match(/msie/i)) {
        e.preventDefault();
//         $('form').find('button[type=submit],input[type=submit]').click();
        $("#btn[value='Refine / Search']").click();
        $("#btn[value='Search']").click()
    }
});

function toggleSlide(id, speed) {
    
    speed = typeof speed !== 'undefined' ? speed : 'fast';
    
    if ($(id).css("display") == 'none') {
        $(id).slideDown(speed);
    }
    else {
        $(id).slideUp(speed);
    }
}

function toggleFadeAtScroll(id, scrollDist) {
    
    if ($.jStorage.get('scrollPosition') > scrollDist && $(id).css("display") == 'none') {
        $(id).fadeIn("slow");
    }
    if ($.jStorage.get('scrollPosition') < scrollDist) {
        $(id).fadeOut("slow");
    }
}

//keep fulltext searchbox checked???
	
function maintainSelect(id, jStoreVar, selectList) {

    if ($.jStorage.get(jStoreVar)) {
        var agencySel = $.jStorage.get(jStoreVar).join(", "); //get stored select-values from previous page filters
        $(id).val($.jStorage.get(jStoreVar)); //set the values for current page
        $(id).next().children('button').attr('title', agencySel); //set value="title" to select-value list
        $(id).next().children('button').children('.filter-option').text(agencySel); //set text to select-value list
        for (var i = 0; i < $.jStorage.get(jStoreVar).length; i++) { //activate each value manually (for tick marks -- purely aesthetic)
            var location = "li[rel='%s']".replace('%s', selectList[$.jStorage.get(jStoreVar)[i]]);
            $(id).next().children('.dropdown-menu').children('ul').children(location).attr('class', 'selected');
        }
    }
}

function deselect(id, noneSelText, selectList) {
	$(id).val('');
	$(id).next().children('button').attr('title', noneSelText);
    $(id).next().children('button').children('.filter-option').text(noneSelText);
	for (var i = 0; i < selectList.length; i++)
		$(id).next().children('.dropdown-menu').children('ul').children("li[rel='%s']".replace('%s', i)).attr('class', '');
}

function storeFilters() {
    if ($('#input_text').val() || !isEmpty($('#input_text').val())) { $.jStorage.set('inputVal', $('#input_text').val()); }
    $.jStorage.set('agencyVal', $('#agencies').val());
    $.jStorage.set('categoryVal', $('#categories').val());
    $.jStorage.set('typeVal', $('#types').val());
}

$("#btn[value='Refine / Search']").click(storeFilters);

$("#btn[value='Search']").click(storeFilters);

$("#btn[value='Remove All']").on('click', function() {
    $("option:selected").removeAttr("selected");
	/*
deselect('#agencies', 'All Agencies', agencies);
	deselect('#categories', 'All Categories', categories);
	deselect('#types', 'All Types', types);
*/
});

//reset jStorage upon redirecting to home page
$("a[href='../index']").on('click', function() {
    $.jStorage.flush();
});

//make sure what is suppose to work works
$('.disabled').click(function(event){
    event.preventDefault();
});
$('.active').click(function(event){
    event.preventDefault();
});

//check if string contains only white space
function isEmpty(str) {
    return str.replace(/^\s+|\s+$/gm,'').length == 0;
}   

/*
$(function () {
    //popover stlyle
    $('.popover-hover').popover( {
        trigger: 'hover',
        html: true,
        placement: 'top',
    });
    
    $('.popover-hover-right').popover( {
        trigger: 'hover',
        html: true,
        placement: 'right',
    });
*/
    
    //submit if valid
    $('#index-form').submit(function(event) {
        if ( (!$('#input_text').val() || isEmpty($('#input_text').val()) ) && ( !$.jStorage.get('agencyVal') && !$.jStorage.get('categoryVal') && !$.jStorage.get('typeVal') ) ) {
           event.preventDefault();
           document.getElementById("search_error").style.display= "block";
           $('#input_text').css({'border-color':'#FF0000', 'box-shadow':'0 0 10px #FF0000'}).addClass('form-control-danger');
        }
    });
    
    $('#result-form').submit(function(event) {
        if ( (!$.jStorage.get('inputVal') || isEmpty($.jStorage.get('inputVal')) ) && ( !$.jStorage.get('agencyVal') && !$.jStorage.get('categoryVal') && !$.jStorage.get('typeVal') ) ) {
           event.preventDefault();
           document.getElementById("search_error").style.display= "block";
           $('#input_text').css({'border-color':'#FF0000', 'box-shadow':'0 0 10px #FF0000'}).addClass('form-control-danger');
        }
    });
    
// });

$('#sidebar-lock').click( function() {
    $.jStorage.set('sidebarLocked', !$.jStorage.get('sidebarLocked') );
    $(this).toggleClass('btn-default');
});

//toggles search options and result margins
$('[data-toggle="offcanvas"]').click(function () {
    if (!$.jStorage.get('sidebarLocked')) {
        if ($(window).width() > 767) {
            if ( $('#results').css('margin-right') == '0px') {
                $('#results').animate( { marginRight: "275px" }, 200, function() {
                    $('.options').slideToggle('fast');
                });
            }
            else {
                $('.options').slideToggle('fast', function() {
                    $('#results').animate( { marginRight: "0px" }, 200);    
                });
            }
        }
        else {
            $('.options').slideToggle('fast');
        }
    }
});

$(window).resize( function() {
    if ($(window).width() > 767) {
        if ($('.options').css('display') != 'none' && $('#results').css('margin-right') != "275px") {
            $('#results').css( { marginRight: "275px" });
        }
        if ($('.options').css('display') == 'none' && $('#results').css('margin-right') != "0px") {
            $('#results').css( { marginRight: "0px" });
        }
    }
    else {
        if ($('#results').css('margin-right') != "-15px") {
            $('#results').css( { marginRight: "-15px" });
        }
    }
    
    $('body').css('padding-top', $('#results-info').height() + $('#header').height());
    $('.options').css('padding-top', $('#results-info').height() + $('#header').height());
    
});

//prevents result scrolling when cursor over search options
$('.options').hover( function() {
     $('body').toggleClass('scroll-lock');
});

$('.options').mouseenter( function() {
    $(this).animate({opacity: 1}, 200);
});

$('.options').mouseleave( function() {
    if ($(window).width() < 767) {
        $(this).animate({opacity: 0.5}, 200);
    }
});


$(window).scroll( function() {
    $.jStorage.set('scrollPosition', $('body').scrollTop());
    toggleFadeAtScroll('#2top', 100);
});

$(window).on('load', function () {

    $('body').css('padding-top',$('#results-info').height() + $('#header').height());
    $('.options').css('padding-top', $('#results-info').height() + $('#header').height());
    
    if ($.jStorage.get('sidebarLocked',false)) {
        $('#sidebar-lock').removeClass('btn-default');
        $('.options').css('display','block');
        if ($(window).width() > 767) {
            $('#results').css('margin-right','275px');
        }
    }
    
    toggleSlide('#search-area', 'slow');
    
    var agencies = {"Aging": 0, "Buildings": 1, "Campaign Finance": 2, "Children's Services": 3, "City Council": 4, "City Clerk": 5, "City Planning": 6, "Citywide Admin Svcs": 7, "Civilian Complaint": 8, "Comm - Police Corr": 9, "Community Assistance": 10, "Comptroller": 11, "Conflicts of Interest": 12, "Consumer Affairs": 13, "Contracts": 14, "Correction": 15, "Criminal Justice Coordinator": 16, "Cultural Affairs": 17, "DOI - Investigation": 18, "Design/Construction": 19, "Disabilities": 20, "District Atty, NY County": 21, "Districting Commission": 22, "Domestic Violence": 23, "Economic Development": 24, "Education, Dept. of": 25, "Elections, Board of": 26, "Emergency Mgmt.": 27, "Employment": 28, "Empowerment Zone": 29, "Environmental - DEP": 30, "Environmental - OEC": 31, "Environmental - ECB": 32, "Equal Employment": 33, "Film/Theatre": 34, "Finance": 35, "Fire": 36, "FISA": 37, "Health and Mental Hyg.": 38, "HealthStat": 39, "Homeless Services": 40, "Hospitals - HHC": 41, "Housing - HPD": 42, "Human Rights": 43, "Human Rsrcs - HRA": 44, "Immigrant Affairs": 45, "Independent Budget": 46, "Info. Tech. and Telecom.": 47, "Intergovernmental": 48, "International Affairs": 49, "Judiciary Committee": 50, "Juvenile Justice": 51, "Labor Relations": 52, "Landmarks": 53, "Law Department": 54, "Library - Brooklyn": 55, "Library - New York": 56, "Library - Queens": 57, "Loft Board": 58, "Management and Budget": 59, "Mayor": 60, "Metropolitan Transportation Authority": 61, "NYCERS": 62, "Operations": 63, "Parks and Recreation": 64, "Payroll Administration": 65, "Police": 66, "Police Pension Fund": 67, "Probation": 68, "Public Advocate": 69, "Public Health": 70, "Public Housing-NYCHA": 71, "Records": 72, "Rent Guidelines": 73, "Sanitation": 74, "School Construction": 75, "Small Business Svcs": 76, "Sports Commission": 77, "Standards and Appeal": 78, "Tax Appeals Tribunal": 79, "Tax Commission": 80, "Taxi and Limousine": 81, "Transportation": 82, "Trials and Hearings": 83, "Veterans - Military": 84, "Volunteer Center": 85, "Voter Assistance": 86, "Youth & Community": 87};
    var categories = {"Business and Consumers": 0, "Cultural/Entertainment": 1, "Education": 2, "Environment": 3, "Finance and Budget": 4, "Government Policy": 5, "Health": 6, "Housing and Buildings": 7, "Human Services": 8, "Labor Relations": 9, "Public Safety": 10, "Recreation/Parks": 11, "Sanitation": 12, "Technology": 13, "Transportation": 14};
    var types = {"Annual Report": 0, "Audit Report": 1, "Bond Offering - Official Statements": 2, "Budget Report": 3, "Consultant Report": 4, "Guide - Manual": 5, "Hearing - Minutes": 6, "Legislative Document": 7, "Memoranda - Directive": 8, "Press Release": 9, "Serial Publication": 10, "Staff Report": 11, "Report": 12};

    maintainSelect('#agencies', 'agencyVal', agencies);
    maintainSelect('#categories', 'categoryVal', categories);
    maintainSelect('#types', 'typeVal', types);
    
    $('.pagination').on('click', function() {
    	$.jStorage.set('scrollPosition',0);
    });
    //make sure paginate works appropriately to boostrap css standard
    $('.pagination').children('ul').attr('class', 'pagination');

    $.jStorage.set('prevAgency', $('#agencies').val())
    $.jStorage.set('prevCategory', $('#categories').val())
    $.jStorage.set('prevType', $('#types').val())

});
