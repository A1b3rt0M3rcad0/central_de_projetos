document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const cpf = document.getElementById("cpf").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ cpf, password })
            });

            const data = await response.json();

            if (response.status === 200 && data.access_token) {
                window.location.href = "/dashboard"; // Colocar aqui a rota home de acesso principal
            } else {
                showError("CPF ou senha inválidos.");
            }
        } catch (error) {
            showError("Erro na conexão com o servidor.");
            console.error(error);
        }
    });

    function showError(message) {
        let errorDiv = document.getElementById("error-message");
        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.id = "error-message";
            errorDiv.className = "bg-red-100 text-red-700 p-2 rounded mt-4 text-sm";
            form.parentNode.insertBefore(errorDiv, form);
        }
        errorDiv.innerText = message;
    }
});