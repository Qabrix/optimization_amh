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

func int_in_list(a int, list []int) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func path_in_tabu(path []int, T [][]int) bool {
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

func make_range(min, max int) []int {
	a := make([]int, max-min+1)
	for i := range a {
		a[i] = min + i
	}
	return a
}

func distance(x [][]int, path []int) int {
	current := 0
	res := 0
	for i := 0; i <= len(path); i++ {
		res += x[current][path[i%len(path)]]
		current = path[i%len(path)]
	}

	return res
}

func find_first_path(x [][]int) []int {
	cities := make_range(1, len(x)-1)
	path := []int{0}
	current := 0
	for i := 0; i < len(cities); i++ {
		best := -1
		val := 1000000
		var possible []int
		for _, t := range cities {
			if !int_in_list(t, path) {
				possible = append(possible, t)
			}
		}
		for _, c := range possible {
			if 0 < x[current][c] && x[current][c] < val {
				val = x[current][c]
				best = c
			}
		}

		path = append(path, best)
		current = best
	}
	return path
}

func swap_random(path, T_index []int, step int) []int {
	rand.Seed(time.Now().UnixNano())
	copy_path := append([]int(nil), path...)
	for i := 2; i < len(copy_path); i += step {
		p := rand.Intn(i-1) + 1
		if int_in_list(i, T_index) || int_in_list(p, T_index) {
			continue
		}

		copy_path[i], copy_path[p] = copy_path[p], copy_path[i]
	}

	return copy_path
}

func two_opt(x [][]int, path []int) []int {
	improved := true
	var new_path, slice []int
	for improved {
		improved = false
		for i := 1; i < len(path)-2; i++ {
			for j := i + 1; j < len(path); j++ {
				if j-i == 1 {
					continue
				}

				new_path = append([]int(nil), path...)
				slice = new_path[i:j]
				for k := len(slice)/2 - 1; k >= 0; k-- {
					opp := len(slice) - 1 - k
					slice[k], slice[opp] = slice[opp], slice[k]
				}

				if distance(x, new_path) < distance(x, path) {
					path = new_path
					improved = true
				}
			}
		}
	}

	return path
}

func two_swap(x, T [][]int, T_index, path, index_fails []int, max_index_fails int) ([][]int, []int, int, []int) {
	var N [][]int
	var copy []int
	var i_val int

	val := distance(x, path)
	best_val := val
	best := append([]int(nil), path...)
	for i := 1; i < len(path)-1; i++ {
		if int_in_list(i, T_index) {
			continue
		}
		for j := i + 1; j < len(path); j++ {
			copy = append([]int(nil), path...)
			copy[i], copy[j] = copy[j], copy[i]
			i_val = distance(x, copy)
			if i_val > val {
				index_fails[i] += 1
				if index_fails[i] > max_index_fails {
					T_index = append(T_index, i)
					break
				}
			}

			if !path_in_tabu(copy, T) {
				N = append(N, copy)
				if i_val < best_val {
					best_val = i_val
					best = copy
				}
			}
		}
	}

	return N, best, best_val, T_index
}

func find_best(x, N [][]int) ([]int, int) {
	best := append([]int(nil), N[0]...)
	val := distance(x, N[0])
	var temp int
	for _, n := range N {
		temp = distance(x, n)
		if temp < val {
			val = temp
			best = n
		}
	}

	return best, val
}

func tabu_search(x [][]int, path []int, time_limit float64, max_e, tabu, tabu_index, max_index_fails int) (int, []int) {
	var T, N [][]int
	var T_index, index_fails []int
	var in_same, temp int

	for i := 0; i < len(path); i++ {
		index_fails = append(index_fails, 0)
	}

	best_val := distance(x, path)
	best_path := append([]int(nil), path...)
	same := 0

	time_delta := 0.0
	time_start := time.Now()

	for time_delta < time_limit {
		rand.Seed(time.Now().UnixNano())
		in_same = 0
		for i := 0; i < max_e; i++ {
			if in_same > max_e/2 {
				in_same = 0
				break
			}

			N, path, temp, T_index = two_swap(x, T, T_index, path, index_fails, max_index_fails)

			if len(N) == 0 {
				break
			}

			T = append(T, N...)
			if len(T) > tabu {
				T = T[len(T)-tabu:]
			}

			if len(T_index) > tabu_index {
				for _, index := range T_index[:len(T_index)-tabu_index-1] {
					index_fails[index] = 0
				}

				T_index = T_index[len(T_index)-tabu_index:]
			}

			path = two_opt(x, path)
			temp = distance(x, path)
			if temp < best_val {
				best_val = temp
				best_path = path
				same = 0
				in_same = 0
			} else {
				same += 1
				in_same = 0
			}
		}

		path = swap_random(path, T_index, rand.Intn(len(path)-1)+1)
		path = two_opt(x, path)
		temp = distance(x, path)

		if temp < best_val {
			best_val = temp
			best_path = path
			same = 0
		} else {
			same += 1
		}

		time_delta = float64(time.Since(time_start)) / math.Pow(10, 9)
		// println(best_val)
		// for _, sa := range T_index {
		// 	print(sa, " ")
		// }
		// println()
	}
	return best_val, best_path
}

func get_input() (float64, int, [][]int) {
	var lines []string
	var mapa [][]int
	var n int
	var time float64

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	temp := strings.Split(lines[0], " ")
	time, _ = strconv.ParseFloat(temp[0], 64)
	n, _ = strconv.Atoi(temp[1])

	for i := 1; i <= n; i++ {
		converted := make([]int, 0)
		for _, num := range strings.Split(lines[i], " ") {
			nc, _ := strconv.Atoi(string(num))
			converted = append(converted, nc)
		}
		mapa = append(mapa, converted)
	}
	return time, n, mapa
}

func main() {
	result_path := ""
	time_limit, n, x := get_input()

	max_e := int(0.5 * float64(n))
	max_fuck_ups := int(math.Pow(float64(n), 2))
	tabu_size := 5 * int(math.Pow(float64(n), 2)/math.Log(float64(n)))
	tabu_index_size := int(n / 10)

	path := find_first_path(x)
	val, result_path_int := tabu_search(x, path, time_limit, max_e, tabu_size, tabu_index_size, max_fuck_ups)

	fmt.Fprintf(os.Stdout, "%d", val)
	for _, step := range result_path_int {
		result_path += strconv.Itoa(step)
	}
	fmt.Fprintf(os.Stderr, "%s", result_path)
}
