# Reinforcement Learning для траектории полного обхода динамической среды

## Задача

Исследовать среду с ограниченным углом обзора.

## Параметры среды

- width: 20 
  
- height: 20
  
- max_rooms: 3 
  
- min_room_xy: 5 

- max_room_xy: 10 

- observation_size: 11

- vision_radius: 5

## PPO, архитектура модели
- Conv2D(in_channels=4, out_channels=16, kernel_size=3, stride=2)
- Conv2D(in_channels=32, out_channels=32, kernel_size=3, stride=2)
- Conv2D(in_channels=32, out_channels=32, kernel_size=3, stride=1)
- Linear(32)
- Linear(out_dim)

Размер выхода модели `out_dim` равен либо action_dim (Actor), либо 1 (Critic).

## Функции награды
В ходе экспериментов были опробованы 3 функции награды:

- Базовая награда reward = $a^2$

## Результаты

