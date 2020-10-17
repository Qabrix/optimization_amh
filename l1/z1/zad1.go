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

const MIN, MAX = -1000.0, 1000.0

type vector struct {
	a, b, c, d, minimum float64
	typ                 bool
}

func random_vector(min, max float64, typ bool) vector {
	rand.Seed(time.Now().UnixNano())
	a := rand.Float64()*(max-min) + min
	b := rand.Float64()*(max-min) + min
	c := rand.Float64()*(max-min) + min
	d := rand.Float64()*(max-min) + min
	vec := vector{a, b, c, d, 0.0, typ}
	vec.minimum = calculate_func(vec)
	return vec
}

func calculate_GW(a, b, c, d float64) float64 {
	var x = [4]float64{a, b, c, d}
	x_sum := 0.0
	x_mul := 1.0
	for i := range x {
		x_sum += math.Pow(x[i], 2)
		x_mul *= math.Cos(x[i] / math.Sqrt(float64(i)+1))
	}

	return 1 + x_sum/4000 - x_mul
}

func calculate_HC(a, b, c, d float64) float64 {
	var l float64 = math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) + math.Pow(d, 2)
	return math.Pow(math.Pow(l-4, 2), 0.125) + (l/2+a+b+c+d)/4 + 0.5
}

func calculate_func(vec vector) float64 {
	if vec.typ {
		return calculate_GW(vec.a, vec.b, vec.c, vec.d)
	} else {
		return calculate_HC(vec.a, vec.b, vec.c, vec.d)
	}
}

func gradient_GW_Speed(vec vector, alpha float64) vector {
	a, b, c, d := vec.a, vec.b, vec.c, vec.d
	ga := a - alpha*(math.Sin(a)*math.Cos(b)*math.Cos(c)*math.Cos(d))/1.0 + a/2000
	gb := b - alpha*(math.Sin(b)*math.Cos(a)*math.Cos(c)*math.Cos(d))/1.0 + b/2000
	gc := c - alpha*(math.Sin(c)*math.Cos(b)*math.Cos(a)*math.Cos(d))/1.0 + c/2000
	gd := d - alpha*(math.Sin(d)*math.Cos(b)*math.Cos(c)*math.Cos(a))/1.0 + d/2000
	return vector{ga, gb, gc, gd, calculate_func(vec), vec.typ}
}

func gradient_HC_Speed(vec vector, alpha float64) vector {
	a, b, c, d := vec.a, vec.b, vec.c, vec.d
	comp1 := (2 * a * (math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4))
	comp2 := 1.0
	x := (comp1/comp2 + a + 1) / 4

	ga := a - alpha*x

	comp1 = (2 * b * (math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4))
	x = (comp1/comp2 + b + 1) / 4

	gb := b - alpha*x

	comp1 = (2 * c * (math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4))
	x = (comp1/comp2 + c + 1) / 4

	gc := c - alpha*x

	comp1 = (2 * d * (math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4))
	x = (comp1/comp2 + d + 1) / 4

	gd := d - alpha*x
	return vector{ga, gb, gc, gd, calculate_func(vec), vec.typ}
}

func gradient_GW(vec vector, alpha float64) vector {
	a, b, c, d := vec.a, vec.b, vec.c, vec.d
	ga := a - alpha*((math.Sin(a)*math.Cos(b)*math.Cos(c)*math.Cos(d))/(2*math.Sqrt(6))+a/2000)
	gb := b - alpha*((math.Sin(b)*math.Cos(a)*math.Cos(c)*math.Cos(d))/(2*math.Sqrt(6))+b/2000)
	gc := c - alpha*((math.Sin(c)*math.Cos(b)*math.Cos(a)*math.Cos(d))/(2*math.Sqrt(6))+c/2000)
	gd := d - alpha*((math.Sin(d)*math.Cos(b)*math.Cos(c)*math.Cos(a))/(2*math.Sqrt(6))+d/2000)
	return vector{ga, gb, gc, gd, calculate_func(vec), vec.typ}
}

func gradient_HC(vec vector, alpha float64) vector {
	a, b, c, d := vec.a, vec.b, vec.c, vec.d
	comp1 := (2 * a * (math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4))
	comp2 := math.Pow((math.Pow((math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4), 2)), 0.875)
	x := (comp1/comp2 + a + 1) / 4

	ga := a - alpha*x

	comp1 = (2 * b * (math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4))
	comp2 = math.Pow((math.Pow((math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4), 2)), 0.875)
	x = (comp1/comp2 + b + 1) / 4

	gb := b - alpha*x

	comp1 = (2 * c * (math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4))
	comp2 = math.Pow((math.Pow((math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4), 2)), 0.875)
	x = (comp1/comp2 + c + 1) / 4

	gc := c - alpha*x

	comp1 = (2 * d * (math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4))
	comp2 = math.Pow((math.Pow((math.Pow(d, 2) + math.Pow(a, 2) + math.Pow(b, 2) + math.Pow(c, 2) - 4), 2)), 0.875)
	x = (comp1/comp2 + d + 1) / 4

	gd := d - alpha*x
	return vector{ga, gb, gc, gd, calculate_func(vec), vec.typ}
}

func choose_gradient_speed(vec vector, alpha float64) vector {
	if vec.typ {
		return gradient_GW_Speed(vec, alpha)
	} else {
		return gradient_HC_Speed(vec, alpha)
	}
}

func choose_gradient(vec vector, alpha float64) vector {
	if vec.typ {
		return gradient_GW(vec, alpha)
	} else {
		return gradient_HC(vec, alpha)
	}
}

func searcher(vec vector, alpha float64, OP_LIMIT int, speed bool) vector {
	var old_minimum float64
	j := 0
	for j < OP_LIMIT {
		old_minimum = vec.minimum
		if speed {
			vec = choose_gradient_speed(vec, alpha)
		} else {
			vec = choose_gradient(vec, alpha)
		}

		vec.minimum = calculate_func(vec)
		if old_minimum == vec.minimum {
			break
		}
		j++
	}
	return vec
}

func find_minimum(vec vector, alpha, start, org_start, min_start, STEP_LIMIT float64, OP_LIMIT int, ocur_limit int) vector {
	t := time.Now()
	best_x, best_x_global := vec, vec
	ocur_count, reset_count, k, min, max := 0, 0, 0.0, 0.0, 0.0
	speed := false

	for k < STEP_LIMIT {
		cur_x := searcher(vec, alpha, OP_LIMIT, speed)
		//fmt.Printf("%f\n", best_x_global.minimum)
		if cur_x.minimum <= best_x.minimum {
			best_x = cur_x
			ocur_count = 0
			reset_count = 0
		} else {
			ocur_count++
			reset_count++
		}

		if ocur_count >= ocur_limit && start > min_start {
			start /= 2
		} else if ocur_count == 0 {
			start = org_start
		}
		if float64(reset_count) >= float64(ocur_limit)*math.Max(math.Abs(MIN)/2, math.Abs(MAX)) || reset_count >= ocur_limit && best_x.minimum >= 1.0 {
			vec = random_vector(MIN, MAX, vec.typ)
			best_x = vec
			ocur_count = 0
			reset_count = 0
			start = org_start
			speed = false
		} else {
			speed_x := searcher(vec, alpha, OP_LIMIT, true)
			if speed_x.minimum < best_x_global.minimum && !speed {
				vec = speed_x
				best_x_global = speed_x
				speed = true
			}

			if ocur_count <= ocur_limit*5 {
				if vec.typ {
					cur_x = best_x
				}
				min = math.Min(cur_x.a, math.Min(cur_x.b, math.Min(cur_x.c, cur_x.d))) - start
				max = math.Max(cur_x.a, math.Max(cur_x.b, math.Max(cur_x.c, cur_x.d))) + start
				vec = random_vector(min, max, vec.typ)
			} else {
				vec = random_vector(min*2, max*2, vec.typ)
				ocur_count = 0
				start = org_start
			}
			if best_x.minimum < best_x_global.minimum {
				best_x_global = best_x
			}
		}
		k = float64(time.Since(t)) / math.Pow(10, 9)
	}

	return best_x_global
}

func get_input() (float64, bool) {
	var lines []string
	var step_limit float64
	var isHC bool

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	temp := strings.Split(lines[0], " ")
	step_limit, _ = strconv.ParseFloat(temp[0], 64)
	isHC, _ = strconv.ParseBool(temp[1])

	return step_limit, isHC
}

func main() {
	step_limit, isHC := get_input()

	alpha := 0.05
	start := 0.01
	min_start := 0.000001
	org_start := start
	ocur_limit := 10
	op_limit := 100

	if isHC {
		alpha = 0.5
		start = 2.0
		min_start = 0.1
		org_start = start
		ocur_limit = 1
		op_limit = 10
	}

	// println("Wylosowany wektor: ")
	vec := random_vector(MIN, MAX, isHC)
	// fmt.Printf("%f %f %f %f\n", vec.a, vec.b, vec.c, vec.d)
	// fmt.Printf("wartosc: %.12f\n", vec.minimum)

	vec = find_minimum(vec, alpha, start, org_start, min_start, step_limit, op_limit, ocur_limit)

	// println("\nZnalezione min: ")
	fmt.Fprintf(os.Stdout, "%.24f %.24f %.24f %.24f %.24f", vec.a, vec.b, vec.c, vec.d, vec.minimum)
}
