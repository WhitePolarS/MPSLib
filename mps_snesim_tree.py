from entity.SNESIMTree import SNESIMTree

if __name__ == "__main__":

    # 绑定参数文件
    parameter_file = "mps_snesim.txt"
    # 用参数文件实例化SNESIMTree
    aSimulation = SNESIMTree(parameter_file)
    # 开始模拟
    aSimulation.startSimulation()
