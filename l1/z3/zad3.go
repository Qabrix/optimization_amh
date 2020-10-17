package main

import (
	"bufio"
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

func path_in_tabu(path []string, T [][]string) bool {
	for _, t := range T {
		for i, p := range t {
			if p != path[i] {
				break
			} else if i == len(path)-1 {
				return true
			}
		}
	}

	return false
}

func get_agent_cords(mapa [][]string, n int, m int) []int {
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			if mapa[i][j] == "5" {
				return []int{i, j}
			}
		}
	}

	return []int{-1, -1}
}

func check_if_valid(dir string, position []int, mapa [][]string) bool {
	if check_if_exited([]int{position[0], position[1]}, mapa) {
		return false
	}

	if dir == "U" {
		if mapa[position[0]-1][position[1]] != "1" {
			return true
		}
	} else if dir == "D" {
		if mapa[position[0]+1][position[1]] != "1" {
			return true
		}
	} else if dir == "L" {
		if mapa[position[0]][position[1]-1] != "1" {
			return true
		}
	} else if dir == "R" {
		if mapa[position[0]][position[1]+1] != "1" {
			return true
		}
	}

	return false
}

func check_if_exited(position []int, mapa [][]string) bool {
	if mapa[position[0]][position[1]] == "8" {
		return true
	}

	return false
}

func returned(step string) string {
	if step == "U" {
		return "D"
	} else if step == "D" {
		return "U"
	} else if step == "L" {
		return "R"
	} else if step == "R" {
		return "L"
	}

	return "err"
}

func make_step(dir string, position []int) []int {
	var cur_pos []int
	if dir == "U" {
		cur_pos = []int{position[0] - 1, position[1]}
	} else if dir == "D" {
		cur_pos = []int{position[0] + 1, position[1]}
	} else if dir == "L" {
		cur_pos = []int{position[0], position[1] - 1}
	} else if dir == "R" {
		cur_pos = []int{position[0], position[1] + 1}
	}

	return cur_pos
}

func make_random_moves(position []int, mapa [][]string, n, m, steps_size int, moves []string) ([]int, []string, int) {
	rand.Seed(time.Now().UnixNano())
	made_steps := 0
	var path []string
	var cur_step, prev string

	way_limit := rand.Intn(int(math.Min(float64(n), float64(m)))-1) + 1

	for made_steps < steps_size {
		cur_step = moves[rand.Intn(len(moves))]
		for cur_step == returned(prev) || !check_if_valid(cur_step, position, mapa) {
			cur_step = moves[rand.Intn(len(moves))]
		}

		for i := 0; i < way_limit; i++ {
			if !check_if_valid(cur_step, position, mapa) {
				break
			}
			position = make_step(cur_step, position)
			made_steps += 1
			path = append(path, cur_step)
			prev = cur_step
			if check_if_exited(position, mapa) {
				return position, path, made_steps
			}
		}
	}

	return position, path, made_steps
}

func analize_path(position []int, path []string, mapa [][]string, n, m int) ([]int, int) {
	steps := 0
	for _, i := range path {
		if check_if_valid(i, position, mapa) {
			position = make_step(i, position)
			steps += 1
		} else {
			return position, steps
		}
	}

	return position, steps
}

func two_swap(path []string, T [][]string, t_limit int) [][]string {
	var N [][]string
	var copy []string
	max := 10
	iter := 0
	for i := 0; i < len(path)-1; i++ {
		for j := 0; j < len(path); j++ {
			if iter > max {
				return N
			}

			copy = path[:]
			copy[i], copy[j] = copy[j], copy[i]
			if !path_in_tabu(copy[:t_limit], T) {
				N = append(N, copy)
				iter += 1
			}
		}
	}

	return N
}

func find_best(N, mapa, T [][]string, pos []int, n, m, t_limit int) ([]string, int, [][]string) {
	var best_path []string
	var cur_pos []int
	var steps int
	best_steps := 0
	for _, p := range N {
		cur_pos, steps = analize_path(pos, p, mapa, n, m)
		if check_if_exited(cur_pos, mapa) {
			if steps < best_steps || steps == 0 {
				best_steps = steps
				best_path = p
			} else {
				T = append(T, p[:t_limit])
			}
		}
	}

	return best_path, best_steps, T
}

func find_exit(mapa [][]string, n, m int, time_limit float64, position []int) ([]string, int) {
	var best_path, path, cur_path []string
	var T, N [][]string
	var pos []int
	var cur_steps int
	moves := []string{"U", "D", "L", "R"}
	start_pos := append([]int(nil), position...)

	best_steps := 0
	t_limit := 5
	steps := 0

	time_delta := 0.0
	time_start := time.Now()

	for time_delta < time_limit {
		pos = start_pos
		path = make([]string, 0)

		for !check_if_exited(pos, mapa) && time_delta < time_limit {
			pos, cur_path, cur_steps = make_random_moves(pos, mapa, n, m, n*m, moves)
			steps += cur_steps
			path = append(path, cur_path...)
			time_delta = float64(time.Since(time_start)) / math.Pow(10, 9)
		}
		if (steps < best_steps && steps != 0) || best_steps == 0 {
			best_steps = steps
			best_path = path
		}

		N = two_swap(path, T, t_limit)

		if len(T) > 100 {
			T = T[len(T)-100:]
		}

		path, steps, T = find_best(N, mapa, T, pos, n, m, t_limit)

		if (steps < best_steps && steps != 0) || best_steps == 0 {
			best_steps = steps
			best_path = path
		}

		time_delta = float64(time.Since(time_start)) / math.Pow(10, 9)
	}
	return best_path, best_steps
}

func get_input() (float64, int, int, [][]string) {
	var lines []string
	var mapa [][]string
	var n, m int
	var time float64
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	temp := strings.Split(lines[0], " ")
	time, _ = strconv.ParseFloat(temp[0], 64)
	n, _ = strconv.Atoi(temp[1])
	m, _ = strconv.Atoi(temp[2])
	for i := 1; i <= n; i++ {
		row := make([]string, 0)
		for _, field := range lines[i] {
			row = append(row, string(field))
		}
		mapa = append(mapa, row)
	}

	return time, n, m, mapa
}

func main() {
	result_path := ""
	time, n, m, mapa := get_input()

	agent := get_agent_cords(mapa, n, m)
	path, s := find_exit(mapa, n, m, time, agent)

	fmt.Fprintf(os.Stdout, "%d", s)
	for _, step := range path {
		result_path += step
	}
	fmt.Fprintf(os.Stderr, "%s", result_path)
}
