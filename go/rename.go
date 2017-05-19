package main

import (
    "flag"
    "log"
    "os"
    "strings"
    "path/filepath"
)

var flagPath = flag.String("path", "", "path to traverse in search of png files.")

func visit(path string, f os.FileInfo, err error) (e error) {
    // if strings.HasPrefix(f.Name(), "txt") {
    log.Println("path",path)
    dir := filepath.Dir(path)
    base := filepath.Base(path)

    newname := filepath.Join(dir, strings.Replace(base, "1", "123", 1))
    log.Printf("mv \"%s\" \"%s\"\n", path, newname)
    os.Rename(path, newname)
    // }
    return
}


func init() {
    flag.Parse()
}

func main() {
    if *flagPath == "" {
        flag.Usage()
        return
    }
    filepath.Walk(*flagPath, visit)
}
