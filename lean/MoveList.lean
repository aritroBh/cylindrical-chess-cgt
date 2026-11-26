import CylChess.Rules

/-! `lake exe movelist`: one position per input line, one output line per position.
The format is specified in `notes/L1.md`; this file is only parsing and printing. -/
open CylChess

def fileChar (f : Nat) : Char := Char.ofNat (97 + f)

def showPawn (c : Color) (p : Pawn) : String :=
  let normalDir := c == .white
  s!"{fileChar p.file}{p.rank}" ++ (if p.up == normalDir then "" else "*")

def showPos (pos : Position) : String :=
  let side (c : Color) := String.join ((pos.pawns c).map fun p => " " ++ showPawn c p)
  let ep := match pos.ep with
    | some (f, r) => s!" / ep {fileChar f}{r}"
    | none => ""
  "W:" ++ side .white ++ " / B:" ++ side .black ++ ep

def showOutcome : Outcome → String
  | .notEnded => "-"
  | .won .white => "W"
  | .won .black => "B"
  | .race .white => "RW"
  | .race .black => "RB"

def showStatus (s : Settings) (b : Board) (pos : Position) : String :=
  match hasPassed s b pos .white, hasPassed s b pos .black with
  | false, false => "-"
  | true, false => "W"
  | false, true => "B"
  | true, true => "WB"

/-- Parse `a4`, `h12`, `c5*` (the `*` marks a pawn moving against its colour's starting direction). -/
def parseSquare (t : String) : Except String (Nat × Nat × Bool) := do
  let cs := t.toList
  let rev := cs.getLast? == some '*'
  let cs := if rev then cs.dropLast else cs
  match cs with
  | c :: rest =>
    unless 'a' ≤ c && c ≤ 'z' do throw s!"bad square {t}"
    match (String.ofList rest).toNat? with
    | some r => pure (c.toNat - 97, r, rev)
    | none => throw s!"bad square {t}"
  | [] => throw "empty square"

def parsePawns (c : Color) (body : String) : Except String (List Pawn) :=
  (body.splitOn " ").filter (· ≠ "") |>.mapM fun t => do
    let (f, r, rev) ← parseSquare t
    pure ⟨f, r, (c == .white) != rev⟩

def parseLine (line : String) : Except String (Settings × Board × Position) := do
  let (head, body) ← match line.splitOn "|" with
    | [h, p] => pure (h, p)
    | _ => throw "expected `<settings> | <position>`"
  let (board, settings) ← match (head.splitOn " ").filter (· ≠ "") with
    | [topo, files, ranks, ep, race] => do
      let topology ← match topo with
        | "flat" => pure Topology.flat | "cyl" => pure .cylinder | "mob" => pure .mobius
        | _ => throw s!"bad topology {topo}"
      let some n := files.toNat? | throw s!"bad files {files}"
      let some m := ranks.toNat? | throw s!"bad ranks {ranks}"
      let epRule ← match ep with
        | "off" => pure EpRule.off | "textbook" => pure .textbook | "aware" => pure .aware
        | _ => throw s!"bad ep option {ep}"
      let raceRule ← match race with
        | "count" => pure RaceRule.count | "mover" => pure .mover | "opponent" => pure .opponent
        | _ => throw s!"bad race rule {race}"
      pure (({ files := n, ranks := m, topology } : Board), (⟨epRule, raceRule⟩ : Settings))
    | _ => throw "expected `<topology> <files> <ranks> <ep> <race>`"
  let parts := (body.splitOn "/").map fun x => x.trimAscii.toString
  let (wPart, bPart, epPart) ← match parts with
    | [w, b] => pure (w, b, none)
    | [w, b, e] => pure (w, b, some e)
    | _ => throw "expected `W: ... / B: ...[ / ep <square>]`"
  unless wPart.startsWith "W:" && bPart.startsWith "B:" do throw "expected `W: ... / B: ...`"
  let white ← parsePawns .white (wPart.drop 2).toString
  let black ← parsePawns .black (bPart.drop 2).toString
  let ep ← match epPart with
    | none => pure none
    | some e =>
      unless e.startsWith "ep " do throw "expected `ep <square>`"
      let (f, r, _) ← parseSquare (e.drop 3).trimAscii.toString
      pure (some (f, r))
  let pos : Position := ⟨white, black, ep⟩
  unless board.valid do throw "invalid board (a cylinder or strip needs at least 3 files)"
  unless pos.valid board do
    throw "invalid position (off board, two pawns on a square, a pawn on its first rank, or a * off the strip)"
  pure (settings, board, pos.normalize settings board)

def sideList (s : Settings) (b : Board) (pos : Position) (c : Color) : String :=
  let kids := (moves s b pos c).map fun q => showPos q ++ " = " ++ showOutcome (classify s b q c)
  let kids := sortBy (fun x y => decide (x < y)) kids
  let tag := if c == .white then "W" else "B"
  s!"{tag}[{kids.length}]:" ++ (if kids.isEmpty then "" else " " ++ " ; ".intercalate kids)

def processLine (line : String) : String :=
  match parseLine line with
  | .error e => "error: " ++ e
  | .ok (s, b, pos) =>
    showPos pos ++ " | " ++ showStatus s b pos ++ " | " ++ sideList s b pos .white ++ " | "
      ++ sideList s b pos .black

partial def loop (stdin : IO.FS.Stream) (stdout : IO.FS.Stream) : IO Unit := do
  let line ← stdin.getLine
  if line.isEmpty then return
  let t := line.trimAscii.toString
  unless t.isEmpty || t.startsWith "#" do
    stdout.putStrLn (processLine t)
  loop stdin stdout

def main : IO Unit := do
  loop (← IO.getStdin) (← IO.getStdout)
