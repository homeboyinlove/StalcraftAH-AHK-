WinGet, pid, pid, STALCRAFT
ControlClick(1351,340,"ahk_pid"pid)

ControlClick(X, Y, WinTitle="", WinText="", ExcludeTitle="", ExcludeText="")
{
  hwnd:=ControlFromPoint(X, Y, WinTitle, WinText, cX, cY
                             , ExcludeTitle, ExcludeText)
  PostMessage, 0x200, 0, cX&0xFFFF | cY<<16,, ahk_id %hwnd% ; WM_MOUSEMOVE
  PostMessage, 0x2A1, 0, cX&0xFFFF | cY<<16,, ahk_id %hwnd% ; WM_MOUSEHOVER
  PostMessage, 0x201, 0, cX&0xFFFF | cY<<16,, ahk_id %hwnd% ; WM_LBUTTONDOWN
  PostMessage, 0x202, 0, cX&0xFFFF | cY<<16,, ahk_id %hwnd% ; WM_LBUTTONUP
 }

ControlFromPoint(X, Y, WinTitle="", WinText="", ByRef cX="", ByRef cY="", ExcludeTitle="", ExcludeText="")
{
    if !(hwnd := WinExist(WinTitle, WinText, ExcludeTitle, ExcludeText))
        return false
  
    VarSetCapacity(pt,8)
    VarSetCapacity(wi,60), NumPut(60,wi)
    DllCall("GetWindowInfo","uint",hwnd,"uint",&wi)
    NumPut(X + (w:=NumGet(wi,4,"int")) - (cw:=NumGet(wi,20,"int")), pt,0)
    NumPut(Y + (h:=NumGet(wi,8,"int")) - (ch:=NumGet(wi,24,"int")), pt,4)
  
    Loop {

        child := DllCall("ChildWindowFromPointEx","uint",hwnd,"int64",NumGet(pt,0,"int64"),"uint",0x5)
        if !child or child=hwnd
            break
        DllCall("MapWindowPoints","uint",hwnd,"uint",child,"uint",&pt,"uint",1)
        hwnd := child
    }
    cX := NumGet(pt,0,"int")
    cY := NumGet(pt,4,"int")
   return hwnd
}