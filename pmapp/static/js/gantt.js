    {/* //var gant_tasks = {{ gantt_all_tasks|tojson }}; */}
    console.log(gant_tasks)

{/* //task_list=[] - I've been swapping bewteen inputs depending on the situation */}
task_list=gant_tasks
var task_list_len = task_list.length;

var gantt_start_date = new Date("2020-01-01 00:00:00.000000");
var gantt_end_date = new Date("2020-02-07 00:00:00.000000");
var gantt_total_days = ((gantt_end_date.getTime() - gantt_start_date.getTime()) / (1000 * 3600 * 24)) + 1;
var gantt_total_days = Math.ceil( gantt_total_days ); 
console.log(gantt_total_days);

//Get a list of people
var flags = [], resource_names = [], l = task_list_len, i;
for( i=0; i<l; i++) {
    if( flags[task_list[i]["resource"]]) continue;
    flags[task_list[i]["resource"]] = true;
    resource_names.push(task_list[i]["resource"]);
};
console.log(resource_names);

//Get a list of projects
var flags = [], project_names = [], l = task_list_len, i;
for( i=0; i<l; i++) {
    if( flags[task_list[i]["project_title"]]) continue;
    flags[task_list[i]["project_title"]] = true;
    project_names.push(task_list[i]["project_title"]);
};
console.log(project_names);

// Make a list of graphable rectangles of tasks that exist between start/end dates, and by person.
rectangles = [];
for (i=0;i<resource_names.length; i++){
     //console.log(resource_names[i]);
     for (j=0;j<task_list_len;j++){
         if (task_list[j]["resource"] == resource_names[i]){
             this_start = new Date(task_list[j]["start_date"]);
             this_end = new Date(task_list[j]["end_date"]);
             //this_end =task_list[j]["end_date"];
             //this_start =task_list[j]["start_date"];
             this_resource = i;
             this_desc = task_list[j]["task_description"];
             this_rect = [this_start,this_end,this_resource,this_desc];
             if (this_start < gantt_end_date){  // These two ifs are to see if this task has any times between gantt stat and gantt end
                 if (this_end > gantt_start_date){
                     if (this_start < gantt_start_date){  // if stat/end are out of bounds, adjust them to fit.
                         this_start = gantt_start_date;
                     };
                     if (this_end > gantt_end_date){
                         this_end = gantt_end_date;
                     };
                     this_start = (this_start-gantt_start_date); // we are adjusting dates to graphable numbers.
                     this_end = (this_end-gantt_start_date);
                     this_start = (this_start/ (1000 * 3600 * 24));
                     this_end = (this_end/ (1000 * 3600 * 24));
                     this_rect = [this_start,this_end,this_resource,this_desc]; // slopping rectangle data into a variable
                 }
             }
             //console.log(this_rect)
             rectangles.push(this_rect);
         }
        }
    }

//setup chart stuff
outside_x= 730;
margin_x = 30;
margin_y = 30;
lables_side = 100;
title_y= 20;
lables_day = 30;
day_width = ((outside_x - (margin_x*2) - lables_side)/(gantt_total_days+1));
day_height = 50;
day_gap = 5;
outside_y = (resource_names.length*(day_height+day_gap)+day_gap+ lables_day+margin_y+margin_y);
first_row = (margin_y+title_y+lables_day)
//labels_text = d3.axisLeft(day_height+day_gap).ticks(resource_names.length);

var svg = d3.select(".gantt_house").append("svg").attr("height",outside_y).attr("width",outside_x);

var g = svg.selectAll(".rect")
  .data(rectangles)
  .enter()
  .append("g")
  .classed('rect', true)
 
  g.append("rect")
  .attr("width", d=> ( d[1] - d[0] + 1)*day_width )
  .attr("height", day_height)
  .attr("x", d=> (margin_x+lables_side) + (d[0]*day_width) )
  .attr("y", d=> first_row + d[2]*(day_height+day_gap))
  .attr("fill",  "#ff6700")


  for( i=0; i<resource_names.length; i++) {
  text = svg.append('text').text(resource_names[i])
                .attr('x', margin_x)
                .attr('y', first_row + (i*(day_height+day_gap)) + ((day_height+day_gap)/2))
                .attr('fill', 'black')
                .attr("font-size", "10px")
  }

  function incDate(date, numdays){
      outdate = new Date(date.getTime() + numdays*(1000 * 3600 * 24));
      out_year = outdate.getFullYear();
      out_day= outdate.getDate();
      out_month= (outdate.getMonth() + 1);
      return_date = `${out_year}-${out_month}-${out_day}`
      return(return_date)}

  for( i=0; i<gantt_total_days; i++) {
  text = svg.append('text').text( incDate(gantt_start_date, i) )
                .attr('x', margin_x+lables_side+(i*day_width))
                .attr('y', first_row - (10*(i%4)))
                .attr('fill', 'black')
                .attr("font-size", "10px")
  }

    text = svg.append('text').text(`All Projects`)
                .attr('x', margin_x)
                .attr('y', title_y)
                .attr("font-size", "20px")

/* //Add the text attributes
var textLabels = text
attr("x", function(d) { return d.cx; })
 .attr("y", function(d) { return d.cy; })
.text( function (d) { return "( " + d.cx + ", " + d.cy +" )"; })
.attr("font-family", "sans-serif")
.attr("font-size", "20px")
.attr("fill", "red"); */
 