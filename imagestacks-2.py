from matplotlib.pyplot import Figure
from matplotlib.animation import FuncAnimation

def create_animation(stack, sizex, sizey, *, p_bar = None, stack2 = None ):
    n_proj = stack.shape[0]
    
    if stack2 is None:
        fig = Figure( figsize=(sizex,sizey))
        sub = fig.subplots()
    else:
        fig = Figure( figsize=(2*sizex,sizey))
        sub, sub2 = fig.subplots(1,2)
            
    fl = stack.flatten()
    v_min= min(fl)
    v_max= max(fl)
    img = sub.imshow(stack[0], interpolation='none', aspect='auto', cmap='gray', vmin=v_min, vmax=v_max)
    img.axes.get_xaxis().set_visible(False)
    img.axes.get_yaxis().set_visible(False)
    
    if stack2 is not None:
        sub.set_title("Original")
        fl = stack2.flatten()
        v_min= min(fl)
        v_max= max(fl)
        img2 = sub2.imshow(stack2[0], interpolation='none', aspect='auto', cmap='gray', vmin=v_min, vmax=v_max)
        img2.axes.get_xaxis().set_visible(False)
        img2.axes.get_yaxis().set_visible(False)
        sub2.set_title("Reconstructed")
    
    if(p_bar is not None):
        p_bar.value=1
        p_bar.max=n_proj+1

    def anim_update(tomo_img):
        if(p_bar is not None):
            p_bar.value+=1
            
        img.set_data(tomo_img)
        return img,
    
    def anim_update2(tomo_img):
        if(p_bar is not None):
            p_bar.value+=1
            
        img.set_data(tomo_img[0])
        img2.set_data(tomo_img[1])
        return img, img2
    
    if stack2 is None:
        anim = FuncAnimation(fig, anim_update, frames=stack)
    else:
        anim = FuncAnimation(fig, anim_update2, frames=zip(stack, stack2), save_count=n_proj)
    return anim