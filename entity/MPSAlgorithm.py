import random
from time import process_time
import numpy as np
from abc import ABC, abstractmethod
from utils.FileUtil import write_sgems_file
from utils.utility import threeD_to_1D, oneD_to_3D, is_nan, secondsToHrMnSec


class MPSAlgorithm(ABC):

    def __init__(self):
        """
        构造函数
        """
        print("1:成功继承")
        self._sg = []  # The simulation grid
        self._hdg = []  # The hard data grid (same size as simulation grid)
        self._tg1 = []  # Temporary grid 1 - meaning define by type of sim-algorithm (same size as simulation grid)
        self._tg2 = []  # Temporary grid 2 - meaning define by type of sim-algorithm (same size as simulation grid)
        self._hd_search_radius = 0.0  # hard data search radius for multiple grids
        self._sg_iterations = []  # 用于调试的模拟网格的副本，用于计算迭代次数
        self._simulation_path = []  # The simulation path
        self._total_grids_level = 0  # multiGrids  levels
        self._sg_dim_x = 0  # Dimension X of the simulation Grid
        self._sg_dim_y = 0  # Dimension Y of the simulation Grid
        self._sg_dim_z = 0  # Dimension Z of the simulation Grid
        self._sg_world_min_x = 0.0  # Coordinate X Min of the simulation grid in world coordinate
        self._sg_world_min_y = 0.0  # Coordinate Y Min of the simulation grid in world coordinate
        self._sg_world_min_z = 0.0  # Coordinate Z Min of the simulation grid in world coordinate
        self._sg_cell_size_x = 0.0  # 在坐标系中x轴方向的单元格大小
        self._sg_cell_size_y = 0.0  # 在坐标系中Y轴方向的单元格大小
        self._sg_cell_size_z = 0.0  # 在坐标系中Z轴方向的单元格大小
        self._max_cond_data = 0  # Maximum conditional data allowed
        self._shuffle_sg_path = 0  # Define type of random simulation grid path
        self._shuffle_entropy_factor = 0  # 定义随机模拟路径的熵因子
        self._realization_numbers = 0  # 创建实现数量
        '''
        * @ brief
        如果在调试模式下，将创建一些额外的文件和信息
        *可以使用不同级别的调试：
        *-1: 没有信息
        *0: 在控制台上显示已用时间
        *1: 在控制台上有网格预览
        *2: 额外的文件被导出（迭代计数器）到输出文件夹
        '''
        self._debug_mode = 0
        self._self_show_preview = False  # Show the simulation grid result in the console
        self._seed = 0.0  # Initial value of the simulation
        self._max_iterations = 0  # 最大迭代次数
        self._ti_dim_x = 0  # Dimension X of the training image
        self._ti_dim_y = 0  # Dimension Y of the training image
        self._ti_dim_z = 0  # Dimension Z of the training image
        self._max_neighbours = 0  # Maximum neighbour allowed when doing the neighbour search function
        self._shuffle_ti_path = True  # Make a random training image path
        self._ti_path = []  # Training image search path
        self._number_of_threads = 0  # Maximum threads used for the simulation
        self._ti_filename = ""  # Training image's filename
        self._output_directory = ""  # Output directory to store the result
        self._hardData_filenames = ""  # Hard data filenames used for the simulation
        self._softData_filenames = [""]  # Soft data filenames used for the simulation
        self._softData_categories = []  # Soft data categories
        self._softData_grids = []  # SoftData grid
        self._TI = []  # The training image
        self._threads = []  # 线程
        self._job_done = False  # 用于同步线程的原子标志

    @abstractmethod
    def _simulate(self, sg_idx_x, sg_idx_y, sg_idx_z, level):
        """
        在MPSAlgorithm类里面的虚函数，本身并未实现，通过子类重写后调用
        :param sg_idx_x:
        :param sg_idx_y:
        :param sg_idx_z:
        :param level:
        :return:
        """
        print("16:失败：进入了父类的方法")

    @abstractmethod
    def _InitStartSimulationEachMultipleGrid(self, level):
        """
        在MPSAlgorithm类里面的虚函数，本身并未实现，通过子类重写后调用
        :param level:
        :return:
        """
        print("10:失败：进入了父类的方法")

    def startSimulation(self):
        """
        开始模拟
        :return:
        """
        print("5:开始模拟")
        if self._debug_mode > -2:
            print("__________________________________________________________________________________")
            print("MPSlib: a C++ library for multiple point simulation")
            print("(c) 2015-2016 I-GIS (www.i-gis.dk) and")
            print("              Solid Earth Geophysics, Niels Bohr Institute (http://imgp.nbi.ku.dk)")
            print("This program comes with ABSOLUTELY NO WARRANTY;")
            print("This is free software, and you are welcome to redistribute it")
            print("under certain conditions. See 'COPYING.LESSER'for details.")
            print("__________________________________________________________________________________")
        # 是否初始化随机种子，else不写，在random.random()时就可以自动生成
        if self._seed != 0:
            random.seed(self._seed)

        # 获取输出文件名
        def find_last(search, target):
            """
            找到某字符串中指定字符最后出现的位置
            :param search: 需要搜索的字符串
            :param target: 用来搜索的字符
            :return: 该字符串中最后出现指定字符的位置，没有则返回-1
            """
            # 找到第一个字符所在位置
            pos = search.find(target)
            # 继续找
            while pos >= 0:
                # 从之前找到的位置 + 1开始找
                next_pos = search.find(target, pos + 1)
                if next_pos == -1:
                    # 没找到就直接返回
                    break
                pos = next_pos
            return pos

        # 用/和\分别匹配路径，谁在后面就用谁
        found1 = find_last(self._ti_filename, "/")
        found2 = find_last(self._ti_filename, "\\")
        found = found1 if found1 > found2 else found2
        output_filename = self._output_directory + "/" + self._ti_filename[found + 1:]
        print("6:输出文件名：{}".format(output_filename))

        # 开始模拟
        total_seconds = 0
        allocatedNodesFromHardData = []
        nodeToPutBack = []
        last_progress = 0
        node_cnt = 0
        total_nodes = 0

        self._sg_iterations = np.full([self._sg_dim_z, self._sg_dim_y, self._sg_dim_x], -1, dtype=float)
        self._sg = np.full([self._sg_dim_z, self._sg_dim_y, self._sg_dim_x], -1, dtype=float)
        for i in range(0, self._realization_numbers):
            # 记录开始模拟的时间
            begin_realization = process_time()
            print("7:开始模拟时间：{}".format(begin_realization))

            self._initializeSG(self._sg_iterations, self._sg_dim_x, self._sg_dim_y, self._sg_dim_z, 0)
            self._initializeSG(self._sg, self._sg_dim_x, self._sg_dim_y, self._sg_dim_z)
            #
            # if self._debug_mode > 1:
            #     self._initializeSG(self._tg1, self._sg_dim_x, self._sg_dim_y, self._sg_dim_z, 0)
            #     self._initializeSG(self._tg2, self._sg_dim_x, self._sg_dim_y, self._sg_dim_z, 0)
            print(self._sg)
            # 多层网格
            for level in range(self._total_grids_level, -1, -1):
                print("9:进入多层网格{}".format(level))
                self._InitStartSimulationEachMultipleGrid(level)

                # 对于从粗到细的每个空间级别
                offset = int(pow(2, level))  # 8-> 4 -> 2 -> 1

                # 为每个级别SG定义模拟路径
                if self._debug_mode > -1:
                    print("Define simulation path for each level ")
                self._simulation_path.clear()
                node_cnt = 0
                # **这一句之后看一下
                total_nodes = int(self._sg_dim_x / offset) * int(self._sg_dim_y / offset) * int(
                    self._sg_dim_z / offset)  # 0 -> 0 -> 0 ->6400
                # print(self._sg_dim_x, total_nodes)

                # print(self._ti_filename)
                # print(self._hardData_filenames)
                print(self._hdg[0][57][3])
                for z in range(0, self._sg_dim_z, offset):
                    for y in range(0, self._sg_dim_y, offset):
                        for x in range(0, self._sg_dim_x, offset):
                            sg_1D_idx = threeD_to_1D(x, y, z, self._sg_dim_x, self._sg_dim_y)
                            self._simulation_path.append(sg_1D_idx)
                            if self._hdg.size != 0 and is_nan(self._sg[z][y][x]):
                                self._sg[z][y][x] = self._hdg[z][y][x]

                if self._debug_mode > 2:
                    output_filepath = output_filename + ".gslib"
                    write_sgems_file(output_filepath, self._sg, self._sg_dim_z, self._sg_dim_y, self._sg_dim_x)
                    self._showSG()
                # Shuffle simulation path indices vector for a random path
                if self._debug_mode > -1:
                    print("Shuffling simulation path using type {}".format(self._shuffle_sg_path))
                #
                # 如果没有软数据则返回随机路径
                if len(self._softData_grids) == 0 and self._shuffle_sg_path == 2:
                    print("WARNING: no soft data found, switch to random path")
                    self._shuffle_sg_path = 1
                #
                # 打乱
                if self._shuffle_sg_path == 1:
                    # 随机打乱
                    print(self._simulation_path)
                    random.shuffle(self._simulation_path)
                    # print("打乱之后的模拟顺序为{}".format(self._simulation_path))
                else:
                    # shuffling preferential to soft data
                    # **待实现
                    self._shuffleSgPathPreferentialToSoftData(level)

                # 执行模拟
                # 对路径中的每个值
                progression_cnt = 0
                total_nodes = int(len(self._simulation_path))

                if self._debug_mode > 1:
                    print("17:开始每个点的模拟")

                # # 从SG清除分配的数据
                # # _clearSGFromHD(allocatedNodesFromHardData);


                # ---------------------------------------
                # 这里将类变量赋值给局部变量
                simulation_path = self._simulation_path
                sg_dim_x = self._sg_dim_x
                sg_dim_y = self._sg_dim_y
                sg = self._sg

                # for ii in range(0, len(self._simulation_path)):
                for ii in range(0, len(simulation_path)):

                    # 获取结点坐标
                    # SG_idx_z, SG_idx_y, SG_idx_x = oneD_to_3D(self._simulation_path[ii], self._sg_dim_x, self._sg_dim_y)
                    SG_idx_z, SG_idx_y, SG_idx_x = oneD_to_3D(simulation_path[ii], sg_dim_x, sg_dim_y)

                    # print(SG_idx_z, SG_idx_y, SG_idx_x)
                    # print(self._sg)
                    # print(self._sg[SG_idx_z][SG_idx_y][SG_idx_x])

                    # 执行模拟直到没有 NaN 值...
                    # if is_nan(self._sg[SG_idx_z][SG_idx_y][SG_idx_x]):
                    #     self._sg[SG_idx_z][SG_idx_y][SG_idx_x] = self._simulate(SG_idx_x, SG_idx_y, SG_idx_z, level)
                    if is_nan(sg[SG_idx_z][SG_idx_y][SG_idx_x]):
                        sg[SG_idx_z][SG_idx_y][SG_idx_x] = self._simulate(SG_idx_x, SG_idx_y, SG_idx_z, level)
                        # print("模拟出点{},{},{}的值为{}".format(SG_idx_x, SG_idx_y, SG_idx_z, self._sg[SG_idx_z][
                        # SG_idx_y][SG_idx_x]))

                    if self._debug_mode > -1:
                        progress = int(progression_cnt / float(total_nodes) * 100)
                        progression_cnt = progression_cnt + 1
                        if progress % 5 == 0 and progress != last_progress:
                            last_progress = progress
                            end_node = process_time()
                            # print(":结束模拟时间：{}".format(end_node))
                            elapse_node_secs = float(end_node - begin_realization)
                            # print(begin_realization,end_node)
                            node_estimated_secs = int(
                                (elapse_node_secs / float(progression_cnt)) * float(total_nodes - progression_cnt))
                            # print(node_estimated_secs)
                            hours, minutes, seconds = secondsToHrMnSec(node_estimated_secs)
                            if progress > 0:
                                print("level:{} Progression (%):{} finish in {}hours {}minutes {}seconds".format(level,
                                                                                                                 progress,
                                                                                                                 hours,
                                                                                                                 minutes,
                                                                                                                 seconds))

                if self._debug_mode > 2:
                    print(output_filename)
                    # write_sgems_file(output_filename)

                if level != 0:
                    pass
                if self._debug_mode > 2:
                    pass

                if self._debug_mode > 2:
                    pass

                print("-----------------------------------")

            if self._debug_mode > 0:
                self._showSG()

            if self._debug_mode > -1:
                end_realization = process_time()
                print(end_realization)
                elapsed_realization_secs = float(end_realization - begin_realization)
                total_seconds = total_seconds + elapsed_realization_secs
                print("Elapsed time (sec): {}         total:{}".format(elapsed_realization_secs, total_seconds))

            if self._debug_mode > -2:
                # 将结果写入文件
                if self._debug_mode > -1:
                    print("将模拟网格写入硬盘驱动器...")
                write_sgems_file(output_filename + "sg" + str(i) + ".gslib", self._sg, self._sg_dim_z, self._sg_dim_y,
                                 self._sg_dim_x)

        if self._debug_mode > -1:
            hours, minutes, seconds = secondsToHrMnSec(int(total_seconds / self._realization_numbers))
            print("Total simulation time {}s".format(total_seconds))
            print(
                "Average time for {}  simulations (hours:minutes:seconds) : {}:{}:{}".format(self._realization_numbers,
                                                                                             hours, minutes, seconds))

        if self._debug_mode > -1:
            print("Number of threads: {}".format(self._number_of_threads))
            print("Conditional points: {}".format(self._max_neighbours))
            print("Max iterations: {}".format(self._max_iterations))
            print("SG: {} {} {}".format(self._sg_dim_x, self._sg_dim_y, self._sg_dim_z))
            print("TI: {} {} {} {}".format(self._ti_filename, self._ti_dim_x, self._ti_dim_y, self._ti_dim_z))

    def _initializeSG(self, sg, sg_dim_x, sg_dim_y, sg_dim_z, value=np.nan):
        """
        初始化模拟网格
        :param sg:模拟网格
        :param sg_dim_x:self._sg_dim_x
        :param sg_dim_y:self._sg_dim_y
        :param sg_dim_z:self._sg_dim_z
        :param value:默认为nan
        :return:
        """
        print("8：初始化模拟网格")
        # sg = np.full((sg_dim_z, sg_dim_y, sg_dim_x), value)
        # print(sg.shape)
        # print(sg)
        for z in range(0, sg_dim_z):
            for y in range(0, sg_dim_y):
                for x in range(0, sg_dim_x):
                    sg[z][y][x] = value

    def _initilizePath(self, sg_dim_x, sg_dim_y, sg_dim_z, path):
        """
        初始化序列模拟路径
        :param sg_dim_x:模拟网格x维大小
        :param sg_dim_y:模拟网格y维大小
        :param sg_dim_z:模拟网格z维大小
        :param path:序列模拟路径
        :return:
        """
        # Putting sequential indices
        cnt = 0
        for z in range(0, sg_dim_z):
            for y in range(0, sg_dim_y):
                for x in range(0, sg_dim_x):
                    path.append(cnt)
                    cnt = cnt + 1
        print("13:初始化的序列模拟路径为：{}".format(path))

    def _showSG(self):
        for z in range(0, self._sg_dim_z):
            print("Z:{}/{}".format(z + 1, self._sg_dim_z))
            for y in range(0, self._sg_dim_y):
                for x in range(0, self._sg_dim_x):
                    pass


