"""
fake_adp.py
Servidor local que imita a API da ADP com dados fictícios.
Rode com: python fake_adp.py
Fica disponível em: http://localhost:5000
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# ── dados fictícios ────────────────────────────────────────────────
FUNCIONARIOS = [
    {
        "workerID": {"idValue": "00001"},
        "person": {
            "legalName": {
                "formattedName": "Ana Lima",
                "givenName": "Ana",
                "familyName1": "Lima",
            }
        },
        "workerDates": {"originalHireDate": "2021-03-15"},
        "workAssignment": {
            "jobTitle": "Analista de RH",
            "departmentCode": {"shortName": "RH"},
        },
    },
    {
        "workerID": {"idValue": "00002"},
        "person": {
            "legalName": {
                "formattedName": "Carlos Souza",
                "givenName": "Carlos",
                "familyName1": "Souza",
            }
        },
        "workerDates": {"originalHireDate": "2019-07-01"},
        "workAssignment": {
            "jobTitle": "Desenvolvedor Sênior",
            "departmentCode": {"shortName": "TI"},
        },
    },
    {
        "workerID": {"idValue": "00003"},
        "person": {
            "legalName": {
                "formattedName": "Beatriz Santos",
                "givenName": "Beatriz",
                "familyName1": "Santos",
            }
        },
        "workerDates": {"originalHireDate": "2022-11-10"},
        "workAssignment": {
            "jobTitle": "Estagiária de Automação",
            "departmentCode": {"shortName": "TI"},
        },
    },
    {
        "workerID": {"idValue": "00004"},
        "person": {
            "legalName": {
                "formattedName": "Marcos Ferreira",
                "givenName": "Marcos",
                "familyName1": "Ferreira",
            }
        },
        "workerDates": {"originalHireDate": "2018-02-20"},
        "workAssignment": {
            "jobTitle": "Gerente de TI",
            "departmentCode": {"shortName": "TI"},
        },
    },
    {
        "workerID": {"idValue": "00005"},
        "person": {
            "legalName": {
                "formattedName": "Julia Costa",
                "givenName": "Julia",
                "familyName1": "Costa",
            }
        },
        "workerDates": {"originalHireDate": "2023-01-05"},
        "workAssignment": {
            "jobTitle": "Analista Financeira",
            "departmentCode": {"shortName": "Financeiro"},
        },
    },
]


# ── endpoints ──────────────────────────────────────────────────────

@app.route("/auth/oauth/v2/token", methods=["POST"])
def token():
    """Simula a geração do token OAuth2."""
    return jsonify({
        "access_token": "token-fake-adp-local-12345",
        "token_type"  : "Bearer",
        "expires_in"  : 3600,
    })


@app.route("/hr/v2/workers", methods=["GET"])
def workers():
    """Lista funcionários com suporte a $skip, $top e $filter."""
    lista = FUNCIONARIOS.copy()

    # filtro por departamento: $filter=department eq 'TI'
    filtro = request.args.get("$filter", "")
    if "eq '" in filtro:
        dept = filtro.split("eq '")[-1].rstrip("'")
        lista = [
            f for f in lista
            if f["workAssignment"]["departmentCode"]["shortName"] == dept
        ]

    # paginação: $skip e $top
    skip = int(request.args.get("$skip", 0))
    top  = int(request.args.get("$top",  100))
    lista = lista[skip: skip + top]

    return jsonify({"workers": lista})


@app.route("/hr/v2/workers/<matricula>", methods=["GET"])
def worker_por_matricula(matricula):
    """Busca um funcionário pelo ID."""
    resultado = [
        f for f in FUNCIONARIOS
        if f["workerID"]["idValue"] == matricula
    ]
    if not resultado:
        return jsonify({"message": "Não encontrado"}), 404

    return jsonify({"workers": resultado})


@app.route("/time/v2/workers/<matricula>/leave", methods=["POST"])
def registrar_ausencia(matricula):
    """Simula o registro de ausência."""
    body = request.get_json()
    return jsonify({
        "leaveRequest": {
            "leaveRequestID": "LR-2025-0001",
            "workerID"      : matricula,
            "status"        : "PENDING_APPROVAL",
            "leaveType"     : body.get("leaveType"),
            "startDate"     : body.get("startDate"),
            "endDate"       : body.get("endDate"),
        }
    }), 201


if __name__ == "__main__":
    print("Servidor falso da ADP rodando em http://localhost:5000")
    app.run(port=5000, debug=True)
    
