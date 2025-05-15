from ambiente import Ambiente
from recurso import Recurso

def verify_resourcer(model):
    for agent in model.schedule.agents:
            if isinstance(agent, Recurso): 
                #if agent.type != "(E)":
                    return True
    return False

def execute_all_steps(model):
    while model.clock_to_storm > 0:
        model.step()

def execute_until_clean(model):
    flag = True
    cont = 0
    while flag:
        cont += 1
        model.step()
        model.clock_to_storm += 1
        flag = verify_resourcer(model)
        print(f"{cont} passos para finalizar")
        
def execute_step(model):
    model.step()

def display_menu():
    print("\nMENU")
    print("(1) Executar passo")
    print("(2) Executar todos os passos")
    print("(3) Executar ate limpar")
    print("(4) Sair")

# Solicita ao usuário o tamanho da grade
select = int(input("Insira o tamanho da grid:\n-> "))

# Inicializa o modelo com o tamanho especificado
model = Ambiente(select)

# Função de ações para simular o comportamento de um switch-case
def actions(choice, model):
    actions_dict = {
        "1": execute_step,
        "2": execute_all_steps,
        "3": execute_until_clean
    }
    action = actions_dict.get(choice)
    if action:
        action(model)
    else:
        print("Escolha inválida, tente novamente.")

# Loop interativo do menu
while True:
    display_menu()
    choice = input("Escolha uma ação: ")
    model.display_grid()

    if choice == "4":
        print("Saindo...")
        break
    else:
        actions(choice, model)
