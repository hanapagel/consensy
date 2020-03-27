<h2>Poll results</h2>

<h3>{{ poll.title }}</h3>
<p>{{ poll.prompt }}</p>


<!-- Display poll results by response: -->
<!-- TODO: Refactor in JS / JQuery -->
<table>
    <tr>
        <td>Agree:</td>
        <td>{{ result['agr'] }}</td>
    </tr>
    <tr>
        <td>Reservations:</td>
        <td>{{ result['rsv'] }}</td>
    </tr>
    <tr>
        <td>Stand aside:</td>
        <td>{{ result['asd'] }}</td>
    </tr>
    <tr>
        <td>Block:</td>
        <td>{{ result['blk'] }}</td>
    </tr>
</table>


Table: 

for item in result:
    html_string: <section> {{ name }}</section>
    html_string: <section> {{ result[response.response_id]}}    

