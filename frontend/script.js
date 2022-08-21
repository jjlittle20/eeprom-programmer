document.getElementById("write_command").onclick = function () {
  eel.getCommand("write")(function (returned_values) {
    const JSONValues = JSON.parse(returned_values);
    //hex
    const perrow = 16;
    let hexTable = document.createElement("table"),
      row = hexTable.insertRow(),
      cell;
    JSONValues?.hex.forEach((value, i) => {
      cell = row.insertCell();
      cell.innerHTML = value;
      let next = i + 1;
      if (next % perrow == 0 && next != JSONValues?.hex.length) {
        row = hexTable.insertRow();
      }
    });
    document.getElementById("hex_container").appendChild(hexTable);
    //dec
    let decTable = document.createElement("table"),
      decrow = decTable.insertRow(),
      deccell;
    JSONValues?.dec.forEach((value, i) => {
      deccell = decrow.insertCell();
      deccell.innerHTML = value;
      let next = i + 1;
      if (next % perrow == 0 && next != JSONValues?.dec.length) {
        decrow = decTable.insertRow();
      }
    });
    document.getElementById("dec_container").appendChild(decTable);
  });
};
document.getElementById("read_command").onclick = function () {
  eel.getCommand("read")(function (returned_values) {
    const JSONValues = JSON.parse(returned_values);
    const perrow = 1;
    let hexTable = document.createElement("table"),
      row = hexTable.insertRow(),
      cell;
    JSONValues?.hex.forEach((value, i) => {
      cell = row.insertCell();
      cell.innerHTML = value;
      let next = i + 1;
      if (next % perrow == 0 && next != JSONValues?.hex.length) {
        row = hexTable.insertRow();
      }
    });
    document.getElementById("read_hex_container").appendChild(hexTable);
  });
};
