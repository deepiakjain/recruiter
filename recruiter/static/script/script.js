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
});