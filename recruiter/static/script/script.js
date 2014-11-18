// JavaScript Document
$(document).ready(function(){
	$(".search-area .tab-bar .tabs:eq(1)").addClass("selected");
	$(".search-area .search-form:eq(1)").show();
	$(".search-area .tab-bar .tabs").click(function(){
		$(".search-area .tab-bar .tabs").removeClass("selected");
		$(this).addClass("selected");
		var getTabId = $(this).attr("id");
		$(".search-area .search-form").hide();
		$("."+getTabId+"-content").show();
	});
	
	$(".toggle-btns input").click(function(){
		//$(".toggle-btns input").removeClass("active");
		$(this).toggleClass("active");
		if($(this).hasClass("active")){
			$(this).attr("value", "Unlike Profile");
		}else{
			$(this).attr("value", "Like Profile");
		}
	});
});

function update_job_status(url){
    $.ajax({
        url: url
    }).done(function(response) {
        window.location.href = response.url;
    });
}

function update_status(status, job_code, seeker_id){
    $.ajax({
        url: '/jobs/status/' + status + '/' + job_code + '/' + seeker_id
    }).done(function(response) {
        window.location.href = response.url;
    });
}