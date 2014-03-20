var lo_source   = $("#lo-template").html();
var template = Handlebars.compile(lo_source);

var xblock_runtime = null;
var xblock_element = null;

function ConceptXBlock(runtime, element)
{
    xblock_runtime = runtime;
    xblock_element = element;
    init();
}

function update_item(item, slug, full)
{
    item.data('slug',slug);
    item.data('render',full);
    item.mouseover(function() {
	$(".description").html("<h1>"+slug+"</h1><p>"+full+"</p>");
    })
    item.find(".lo_close").mouseup(function(event){item.remove(); dump_state();});
    dump_state();
}

function create_item(slug, full)
{
    var html = template({title:slug, render:full});
    var domitem = $(html);
    update_item(domitem, slug, full);
    
    domitem.draggable({
	appendTo: "body",
	helper: function(event) {return create_item(slug, full);},
	connectToSortable: ".obj_drop",
	drop : function(event, ui) { console.log(ui.helper); console.log(ui.draggable); }
    });
    
    return domitem;
}

function add_search_item(slug, full)
{
    $(".search_results").append(create_item(slug, full));
}

function dump_state()
{
    state = {'taught'   : $("#taught").find(".lo_drag").map(function(){return $(this).data("slug")}).toArray(),
	     'exercised': $("#exercised").find(".lo_drag").map(function(){return $(this).data("slug")}).toArray(),
	     'required' : $("#required").find(".lo_drag").map(function(){return $(this).data("slug")}).toArray()
	    };
    state = JSON.stringify(state);
    console.log(state);

    url = xblock_runtime.handlerUrl(xblock_element, 'update_concept_map');
    $.post(url, state, function(data) {
    }).done( function(data){
    } ).fail( function(data){
    	console.log("Could not save");
    	console.log(state);
    } );
    return state;
}

function refresh_search(search_string)
{
    url = xblock_runtime.handlerUrl(xblock_element, 'relay_handler')
    $.post(url, JSON.stringify({'suffix':'get_concept_list','q':search_string}), function(data) {
	$(".search_results").text("");
	for (var i = 0; i<data.length; i++) {
	    var slug = data[i];
	    url = xblock_runtime.handlerUrl(xblock_element, 'relay_handler')
	    $.post(url, JSON.stringify({'suffix':'get_concept/'+slug}), function(render) {
		add_search_item(slug, render.article);
	    })
	}
    })
}

function populate(column, array) {
    for(i=0; i<array.length; i++) {
    }	
}

function init() {
    $(".obj_drop").sortable({
	connectWith: ".obj_drop",
	update : function(event, ui) { dump_state(); },
	beforeStop: function(event, ui) {
	    update_item(ui.item, ui.helper.data("slug"), ui.helper.data("render"));
	    //console.log(ui.helper.data("slug"));
	    //ui.placeholder.css("border", "5px solid");
	    //ui.item.css("border", "5px solid");
	    //ui.helper.css("border", "5px solid");
	} 
    }).disableSelection();

    concept_map = $.parseJSON($("#initial-concept-map").text())
    populate('required', concept_map.required)
    populate('taught', concept_map.taught)
    populate('exercised', concept_map.exercised)


    refresh_search("");
    
    $(".search_input").change(function(){
	refresh_search($(".search_input").val());
    });
}

$(function() {
    //var html = template({title:"Hello", render:"Hello world example"});
    //$("#foo").html(html);
//    init();
});
