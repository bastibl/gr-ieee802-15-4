function [out] = css_dqpsk_mod(in_I, in_Q)
    assert(length(in_I) == length(in_Q), 'inputs must have equal length');
    qpsk_angles = angle(in_I + 1j*in_Q)-0.25*pi;
    fb_reg = exp(1j*ones(1,4).*pi/4);
    out = zeros(1,length(qpsk_angles));
    for i=1:length(qpsk_angles)
        out(i) = fb_reg(1)*exp(1j*qpsk_angles(i));
        fb_reg(2:end) = fb_reg(1:end-1);
        fb_reg(1) = out(i);        
    end    
end