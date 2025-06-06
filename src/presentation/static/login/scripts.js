document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const cpf = document.getElementById("cpf").value.trim();
        const password = document.getElementById("password").value;

        try {
            const loginResponse = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ cpf, password })
            });

            const loginData = await loginResponse.json();

            if (loginResponse.ok && loginData.token) {
                const token = getCookie("access_token");
                if (!token) {
                    showError(`Token não encontrado no cookie. ${token}`);
                    return;
                }

                const secureResponse = await fetch("/test/secure", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                });

                if (secureResponse.ok) {
                    const secureData = await secureResponse.json();
                    alert(`✅ Sucesso! Dados: ${JSON.stringify(secureData)}`);
                } else {
                    showError("🚫 Erro ao acessar rota protegida.");
                }

            } else {
                showError("🚫 CPF ou senha inválidos.");
            }
        } catch (error) {
            showError("🚫 Erro na conexão com o servidor.");
            console.error(error);
        }
    });

    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        if (match) {
            return match[2].replace(/^"|"$/g, '');
        }
        return null;
    }

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