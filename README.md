# cable-topo-demo2

## gen_topo.py

- 以线缆的描绘入手，进行递归

## gen_topo_from_point.py

优化了算法，以点的描绘入手，进行递归，递归中调用draw_point, 和draw_cable,

- draw_point中区分点类型进行描绘
- draw_cable中区分线类型进行描绘