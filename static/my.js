function deleteTodo(deleteid,id){
    fetch('/delete/'+deleteid, {method: 'DELETE'}).then(response => response.json()).then(data => {
        console.log(data);
        if (data['code']==200){
            document.getElementById("mytable").deleteRow(id+1);
        }
        else{
            alert('item not deleted');
        }

    })
}
function getData(){
    fetch('/todo')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        let tr='';
        if (data.length==0){
            tr = "<tr><td colspan='5'>No data found</td></tr>";
        }
        for (let i = 0; i < data.length; i++) {
        tr += "<tr><td>"+(i+1)+"</td><td>"+data[i]['title']+"</td>"+"<td>"+data[i]['description']+"</td><td>"+data[i]['datecreated']+"</td>"+
        "<td><a href=/update/"+data[i]['id']+" methods='GET' type='button' class='btn btn-outline-dark btn-sm'>Update</a>"+
        "<a onclick='deleteTodo("+[data[i]['id'],i]+")' type='button' class='btn btn-outline-dark btn-sm'>Delete</a></td></tr>";
        }
        document.getElementById("table").innerHTML=tr;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
window.onload=getData()