function updateAssunto(id) {
  const elem = document.getElementById(`assunto_${id}`);
  if (!elem.value) {
    return null;
  }
  const obj = { name: elem.value };

  let ajax = new XMLHttpRequest();
  ajax.open("PUT", `http://localhost:5000/assuntos/edit/${id}`, true);
  ajax.setRequestHeader("Content-Type", "application/json");

  ajax.onload = () => {
    const res = JSON.parse(ajax.responseText);
    console.log("res", res);
    if (!res.error) {
      window.location.href = "/assuntos/";
    } else {
      alert("Erro");
    }
  };

  ajax.onerror = (error) => {
    console.log("ajax error:", error);
  };

  ajax.send(JSON.stringify(obj));
}
